from flask import Flask
from main.blues.index import admin_bp
from config import DevConfig
from ext import db,login_manager
from flask_cors import *

app = Flask(__name__)   #  __name__ : main
CORS(app, supports_credentials=True)  # 解决前后端分离的  跨域问题
app.config.from_object(DevConfig)
db.init_app(app)
login_manager.init_app(app)



# app.add_url_rule("/", view_func=views.index)
app.register_blueprint(admin_bp)


if __name__ == '__main__':
    app.run(port=5001)

