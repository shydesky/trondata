"""The app module, containing the app factory function."""
import os

from flask import Flask
from flask.helpers import get_debug_flag

from backend.extensions import api

from backend.settings import ProdConfig, DevConfig
from backend.utils import Colors
from backend.database import db

from backend import block

def which_config(sleep=None):
    """ 在环境变量中导出USE_CONFIG决定使用哪个配置
    Args:
        sleep (int or None): sleep seconds
    """
    CONFIG_DICT = {
        'prod': ProdConfig,
        'dev': DevConfig,
    }
    environ = os.environ.get('USE_CONFIG', 'dev')
    CONFIG = CONFIG_DICT.get(environ)
    is_debug = get_debug_flag()
    CONFIG = (CONFIG or DevConfig) if is_debug else CONFIG
    print(Colors.BOLD + '\n>>>>>>>>>>>>>>Use config:',
        CONFIG.__name__, '<<<<<<<<<<<<<<<\n' + Colors.ENDC)

    if sleep is not None:
        import time
        time.sleep(sleep)

    return CONFIG

def register_api(app):
    """Register restful api. 可以在这里导入api或者直接在api文件里用api.route"""
    api.init_app(app)
    db.init_app(app)



def create_app(config_object=ProdConfig):
    """An application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)
    register_api(app)
    return app


