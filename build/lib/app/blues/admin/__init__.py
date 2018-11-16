from main.blues import Blueprint
from . import views
admin_bp = Blueprint('index',__name__,url_prefix='/index',template_folder='templates',static_folder='static')

# @admin_bp.route('/')
# def foo():
#     return '<h1>you are foo</h1>'

admin_bp.add_url_rule('/', view_func=views.index)
admin_bp.add_url_rule('/foo', view_func=views.foo)
