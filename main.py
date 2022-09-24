import app, configparser
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

_cfg = configparser.ConfigParser()
_cfg.read('app/config.ini')
config = _cfg['main']

application = DispatcherMiddleware(app.app)
if __name__ == '__main__':
    run_simple(config['host'], int(config['port']), application, use_reloader=False)
