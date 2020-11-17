from flask import Flask
current_app = Flask(__name__)

from .views import account
from .views import user

current_app.register_blueprint(account.ac) # 注册蓝图
current_app.register_blueprint(user.ur)
# current_app.register_blueprint(user.ur, url_prefix ="user")
