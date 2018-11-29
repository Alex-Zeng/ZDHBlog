from main.blues import Blueprint
from . import views


admin_bp = Blueprint('index',__name__,template_folder='templates',static_folder='static')


admin_bp.add_url_rule('/register', endpoint="register", view_func=views.register, methods=["post"])
admin_bp.add_url_rule('/login', endpoint="login", view_func=views.login, methods=["post"])
admin_bp.add_url_rule('/logout', endpoint="logout", view_func=views.logout, methods=["get"])

admin_bp.add_url_rule('/create_project', endpoint="create_project", view_func=views.create_project, methods=["post"])
admin_bp.add_url_rule('/add_request_api', endpoint="add_request_api", view_func=views.add_request_api, methods=["post"])


admin_bp.add_url_rule('/add_file_level', endpoint="add_file_level", view_func=views.add_file_level, methods=["post"])
admin_bp.add_url_rule('/delete_file_level', endpoint="delete_file_level", view_func=views.delete_file_level, methods=["get"])
admin_bp.add_url_rule('/get_project_list', endpoint="get_project_list", view_func=views.get_project_list, methods=["get"])
admin_bp.add_url_rule('/get_api_list', endpoint="get_api_list", view_func=views.get_api_list, methods=["get"])
admin_bp.add_url_rule('/get_file_level', endpoint="get_file_level", view_func=views.get_file_level, methods=["get"])
