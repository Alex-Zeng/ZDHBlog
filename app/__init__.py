from flask import Flask
from app.blues.admin import admin_bp
from config import DevConfig

app = Flask(__name__)   #  __name__ : app
app.config.from_object(DevConfig)
app.register_blueprint(admin_bp)

from app import views
