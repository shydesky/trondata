import types
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect

csrf_protect = CsrfProtect()
db = SQLAlchemy()

api = Api(decorators=[csrf_protect.exempt])    # 去掉csrf保护

def api_route(self, *args, **kwargs):
    """ 给flask api加上route功能，避免直接调用api.add_resource函数了.
    具体请参考crm_backend.employee.api里的使用
    http://flask.pocoo.org/snippets/129/
    """
    def wrapper(cls):
        self.add_resource(cls, *args, **kwargs)
        return cls
    return wrapper

api.route = types.MethodType(api_route, api)
