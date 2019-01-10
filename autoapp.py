"""Create an application instance."""
import logging
import coloredlogs
from flask_sqlalchemy import get_debug_queries
from backend.app import create_app, which_config

CONFIG = which_config()

coloredlogs.DEFAULT_LOG_FORMAT = '%(asctime)s %(name)s[%(funcName)s]-%(levelname)s Line:%(lineno)s  %(message)s'
coloredlogs.install(level=logging.DEBUG if CONFIG.DEBUG else logging.WARNING)

app = create_app(CONFIG)
# @app.after_request
# def after_request(response):
#     """ 记录慢查询
#     https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvi-debugging-testing-and-profiling
#     """
#     for query in get_debug_queries():
#         if query.duration >= app.config.get('DATABASE_QUERY_TIMEOUT', 0.2):
#             if app.config.get('DATABASE_SLOW_QUERY_ECHO', True):
#                 app.logger.warning(
#                     "SLOW QUERY: %s\nParameters: %s\nDuration: %fs\nContext: %s\n" % (
#                         query.statement, query.parameters, query.duration,
#                         query.context
#                     )
#                 )
#     return response