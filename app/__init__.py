import configparser
import json
import os
import requests
import google.auth.transport.requests
from flask import Flask, render_template, redirect, url_for, session, abort, request, jsonify
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
from google.oauth2 import id_token, service_account
from google.cloud import firestore
from functools import wraps
from google.cloud import secretmanager

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

_cfg = configparser.ConfigParser()
_cfg.read('app/config.ini')
config = _cfg['main']

secret_client = secretmanager.SecretManagerServiceClient()

secret_response = secret_client.access_secret_version(request={"name":
"projects/461900355540/secrets/oauth_client_secret/versions/latest"})
CLIENT_SECRET = secret_response.payload.data.decode("UTF-8")

secret_response = secret_client.access_secret_version(request={"name":
"projects/461900355540/secrets/session_secret/versions/latest"})
SESSION_SECRET = secret_response.payload.data.decode("UTF-8")

oauth_client_config = {
    "web":
        {
            "client_id": config["client_id"],
            "project_id": config["project_id"],
            "auth_uri":"https://accounts.google.com/o/oauth2/auth",
            "token_uri":"https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": CLIENT_SECRET,
            "redirect_uris":[
                config["callback_url"]
            ]
        }
    }

#credentials = service_account.Credentials.from_service_account_file(config['sa_key'])
#db = firestore.Client(project=config['project_id'], credentials=credentials)
db = firestore.Client(project=config['project_id'])

flow = Flow.from_client_config(oauth_client_config, scopes=["openid"],

redirect_uri=config["callback_url"])
app = Flask(__name__, static_folder=config['public'], static_url_path='/public')
app.secret_key = SESSION_SECRET

def modtime(path: str) -> str:
    return str(os.path.getmtime(path)).split('.')[0]

def needs_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            print("Not logged in")
            return redirect(url_for('login'))
        else:
            return func(*args, **kwargs)
    return wrapper

@app.context_processor
def inject_template_vars():

    return {
        "modtime_css": modtime('app/public/styles.css'),
        "modtime_js": modtime('app/public/code.js'),
    }

@app.route("/")
@needs_login
def main():
    doc = db.collection("notes").document(session["google_id"]).get()
    contents = {}
    if doc.exists:
        contents = json.dumps(doc.to_dict()["data"]["ops"])
    return render_template('main.html', contents = contents)

@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main"))

@app.route("/g_callback")
def g_callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=config['client_id']
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    return redirect(url_for("main"))

@app.route("/update", methods=['POST'])
@needs_login
def update():
    doc_ref = db.collection("notes").document(session["google_id"])
    doc_ref.set({
        "data": request.json
    })
    return jsonify("")
