from flask import Flask
from app.blues.admin import admin_bp
import config

app = Flask(__name__)
app.config.from_object('config')
app.register_blueprint(admin_bp)

from app import views
