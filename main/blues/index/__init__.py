from main.blues import Blueprint
from . import views


admin_bp = Blueprint('index',__name__,template_folder='templates',static_folder='static')


admin_bp.add_url_rule('/', view_func=views.index, methods=["GET"])
admin_bp.add_url_rule('/json_str', endpoint="json_str", view_func=views.json_str, methods=["get"])
admin_bp.add_url_rule('/register', endpoint="register", view_func=views.register, methods=["post"])
admin_bp.add_url_rule('/login', endpoint="login", view_func=views.login, methods=["post"])
