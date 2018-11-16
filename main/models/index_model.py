from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from utils import create_browser_id
from itsdangerous import URLSafeSerializer
from ext import db
from config import DevConfig

# 用户表
class User(UserMixin,db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    telephone = db.Column(db.String(11), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100))
    status = db.Column(db.SmallInteger, nullable=False, default=1, doc="用户状态，0-禁用，1-启动")
    create_datetime = db.Column(db.DateTime, server_default=db.text("CURRENT_TIMESTAMP"), doc="创建时间")
    update_datetime = db.Column(db.DateTime, nullable=False, server_default=db.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), doc="更新时间")

    def __init__(self, *args, **kwargs):
        self.telephone = kwargs.get('telephone')
        self.username = kwargs.get('username')
        self.password = generate_password_hash(kwargs.get('password'))  # 加密密码
        self.role = kwargs.get('role')

    def __repr__(self):
        """Define the string format for instance of User."""
        return "<Model User `{}`>".format(self.username)

    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)
        return result

    def get_id(self, life_time=None):
        print("------get_id,life_time=", life_time)
        # print(current_app.__name__)
        # key = current_app.config.get("SECRET_KEY", "The securet key by C~C!")  # current app 拿不到
        key = DevConfig.SECURE_KEY
        s = URLSafeSerializer(key)
        browser_id = create_browser_id()
        if not life_time:
            life_time = current_app.config.get("TOKEN_LIFETIME")
        print((self.id, self.username, self.password, browser_id, life_time))
        # token = s.dumps((self.id, self.username, self.password, browser_id, life_time))
        token = s.dumps([self.id, self.username, self.password, browser_id, life_time])

        return token
