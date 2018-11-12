from app.blues import Blueprint
from . import views
admin_bp = Blueprint('admin',__name__,url_prefix='/admin',template_folder='templates',static_folder='static')

# @admin_bp.route('/')
# def foo():
#     return '<h1>you are foo</h1>'

admin_bp.add_url_rule('/', view_func=views.index)
admin_bp.add_url_rule('/foo', endpoint="foo", view_func=views.foo, methods=["GET"]) # endpoint是别名
admin_bp.add_url_rule('/json_str', endpoint="json_str", view_func=views.json_str, methods=["get"]) # endpoint是别名
