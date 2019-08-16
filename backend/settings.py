"""Application configuration."""
import os


class Config(object):
    """Base configuration."""

    SECRET_KEY = os.environ.get(
        'CRM-BACKEND_SECRET', '5NyDfAe4Qa6W2sk2rBXwKSvgNTclj0Q8mOmP4YpbgM0='
    )
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    BCRYPT_LOG_ROUNDS = 13
    ASSETS_DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SENTRY_DSN = 'http://d592a1c37a92417d871466dfc1abb204:ba7392f628ac4004ad194fe479617ab0@172.16.1.173:9000/4'
    WTF_CSRF_ENABLED = False

    MAIL_LIST = ["shydesky@gmail.com"]

    MAIL_DEBUG = False
    BABEL_DEFAULT_TIMEZONE = 'Asia/Shanghai'

    DATABASE_SLOW_QUERY_ECHO = True  # 是否在终端打印慢查询


class ProdConfig(Config):
    """Production configuration."""

    ENV = 'prod'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql://root:q1w2e3r4@crm-prod.cjfrqij7amkp.us-west-1.rds.amazonaws.com:3306/crm_prod?charset=utf8mb4'
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar

    DATABASE_SLOW_QUERY_ECHO = False

class DevConfig(Config):
    """Development configuration."""

    ENV = 'dev'
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'mysql://root:123qweasd@127.0.0.1:3306/tron?charset=utf8mb4'

    SENTRY_DSN = 'http://3b8fd86a45b7421885134adb473146d4:a32176ef5dec4b62aab891cf9b03ea20@192.168.2.16:9000/4'

    DEBUG_TB_ENABLED = True
    ASSETS_DEBUG = True  # Don't bundle/minify static assets

    DATABASE_SLOW_QUERY_ECHO = False
