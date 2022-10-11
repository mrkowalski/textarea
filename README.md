# textarea

## What is this?

## How to start, locally

* `git clone git@github.com:mrkowalski/textarea.git`
* `cd textarea`
* set up python env somehow. I assume https://github.com/pyenv/pyenv-installer: `curl https://pyenv.run | bash`
* `pyenv install 3.10.6`
* `pyenv virtualenv 3.10.6 textarea`
* `pyenv activate textearea`
* `pip install -r requirements.txt`
* Google Cloud setup
  * Create gcp_textarea_service_account.json
* `gunicorn --bind :<TCP_PORT> main:application`

## Other

# Refresh tlds:

`curl https://data.iana.org/TLD/tlds-alpha-by-domain.txt > tld.txt`
