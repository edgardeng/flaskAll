from flask import Blueprint

ac = Blueprint('account', __name__)


# ac = Blueprint('account', __name__, url_prefix='/account')
# 为蓝图指定静态文件目录， 模板目录
# ac = Blueprint('account', __name__,static_folder='', template_folder='')

@ac.before_request()
def before_request():
    print('account before_request')  # 给某个蓝图加


@ac.route('/a')
def view_a():
    return "view_a"


@ac.route('/b')
def view_b():
    return "view_b"
