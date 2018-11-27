from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from utils import create_browser_id
from flask import current_app
from itsdangerous import URLSafeSerializer
from ext import db
from config import DevConfig


# 用户表
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    telephone = db.Column(db.String(100), nullable=False)
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
        "生成token"
        key = current_app.config.get("SECRET_KEY", "The securet key by C~C!")  # current app 拿不到
        s = URLSafeSerializer(key)
        browser_id = create_browser_id()
        if not life_time:
            life_time = current_app.config.get("TOKEN_LIFETIME")
        token = s.dumps([self.id, self.username, self.password, browser_id, life_time])

        return token


# 项目表
class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    env_id = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    create_datetime = db.Column(db.DateTime, server_default=db.text("CURRENT_TIMESTAMP"), doc="创建时间")
    update_datetime = db.Column(db.DateTime, nullable=False, server_default=db.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), doc="更新时间")
    author = db.relationship('User', backref=db.backref('project'))


# 接口表
class Request_api(db.Model):
    __tablename__ = 'request_api'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    req_name = db.Column(db.String(100), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False, )
    file_level_id = db.Column(db.Integer, db.ForeignKey('file_level.id'), nullable=False, )
    req_method = db.Column(db.String(100), nullable=False)
    req_url = db.Column(db.String(100), nullable=False)
    req_data = db.Column(db.Text)
    create_datetime = db.Column(db.DateTime, server_default=db.text("CURRENT_TIMESTAMP"), doc="创建时间")
    update_datetime = db.Column(db.DateTime, nullable=False, server_default=db.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), doc="更新时间")
    # 在Req_api可以通过project(关系名称)关联到project表根据project_id, 同时在Project表也可以通过api,关联到Comment表
    project = db.relationship('Project', backref=db.backref('request_api', order_by=create_datetime.desc()))
    file_level = db.relationship('File_level', backref=db.backref('request_api', order_by=create_datetime.desc()))


# 文件级别
class File_level(db.Model):
    __tablename__ = 'file_level'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False, )
    pro_id = db.Column(db.String(100), nullable=False)
    label = db.Column(db.String(100))
    create_datetime = db.Column(db.DateTime, server_default=db.text("CURRENT_TIMESTAMP"), doc="创建时间")
    update_datetime = db.Column(db.DateTime, nullable=False, server_default=db.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), doc="更新时间")
    project = db.relationship('Project', backref=db.backref('file_level', order_by=create_datetime.desc()))