from flask import render_template, url_for, jsonify, request, session, redirect,make_response,Response,json,g, current_app
from main.models.index_model import User
from ext import db,login_manager,load_user
from flask_login import login_user, login_required, logout_user, current_user
from utils import create_browser_id
from itsdangerous import URLSafeSerializer, BadData, constant_time_compare
from flask_cache import Cache as simple_cache

def index():
    return render_template('index.html')

@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({'status': 0, 'data': {}, 'msg': "未登录"})

def load_token(token):
    # 通过loads()方法来解析浏览器发送过来的token，从而进行初步的验证
    key = current_app.config.get("SECRET_KEY", "The securet key by C~C!")
    try:
        s = URLSafeSerializer(key)
        id, name, password, browser_id, life_time = s.loads(token)
    except BadData:
        print("token had been modified!")
        return None

    # 判断浏览器信息是否改变
    bi = create_browser_id()
    if not constant_time_compare(str(bi), str(browser_id)):
        print("the user environment had changed, so token has been expired!")
        return None

    # 校验密码
    user = User.query.get(id)
    if user:
        # 能loads出id，name等信息，说明已经成功登录过，那么cache中就应该有token的缓存
        token_cache = simple_cache.get(token)
        if not token_cache:  # 此处找不到有2个原因：1.cache中因为超时失效（属于正常情况）；2.cache机制出错（属于异常情况）。
            print("the token is not found in cache.")
            return None
        if str(password) != str(user.password):
            print("the password in token is not matched!")
            simple_cache.delete(token)
            return None
        else:
            simple_cache.set(token, 1, timeout=life_time)  # 刷新超时时长
    else:
        print('the user is not found, the token is invalid!')
        return None
    return user

@login_manager.user_loader
def user_loader(token):
    """
    这里的入参就是get_id()的返回值
    """
    print("----------user_loader, token=", token)
    return load_token(token)


def json_str():
    return jsonify({'status': "李太白",'data':{}, 'words': "十步杀一人，千里不留行。"})


def register(*args, **kwargs):
    """注册"""
    if request.method == 'POST':
        data = request.get_data()
        json_data = json.loads(data.decode("utf-8"))
        telephone = json_data.get('telephone')  # 不开放注册,暂时只能自己用
        username = json_data.get('username')
        password1 = json_data.get('password1')
        password2 = json_data.get('password2')

        if User.query.filter(User.telephone == telephone).first():
            return jsonify({'status': '201', 'data': {}, 'msg': '该手机号码已被注册!'})

        if User.query.filter(User.username == username).first():
            return jsonify({'status': '201', 'data': {}, 'msg': '该用户名已被使用!'})

        if password1 != password2:
            return jsonify({'status': '201', 'data': {}, 'msg': '两次输入的密码不相同,请核对后再次提交!'})

        user1 = User(telephone=telephone, username=username, password=password1)
        db.session.add(user1)
        db.session.commit()
        return jsonify({'status': '201', 'data': {}, 'msg': '注册成功'})

def login(*args, **kwargs):

    if request.method == 'POST':
        data = request.get_data()
        json_data = json.loads(data.decode("utf-8"))
        # telephone = request.form.get('telephone')
        username = json_data.get('username')
        password = json_data.get('password')
        user = User.query.filter(User.username == username).first()

        if not user:
            return jsonify({'status': 0, 'data': {}, 'msg': '用户不存在'})

        if not User.check_password(user,password):
            return jsonify({'status': 0, 'data': {}, 'msg': '用户密码错误,请重新输入'})

        login_user(user)  # 触发session机制，通过user.get_id()就可以获取到token
        g.user = user
        # 完成登录后将token存到缓存中并设置过期时间，后面校验时如果缓存中不存在，则报错
        life_time = current_app.config.get("TOKEN_LIFETIME")
        token = user.get_id(life_time)
        print("-------- login, token=", token)
        simple_cache.set(token, 1, life_time)

        return jsonify({'status': 1, 'data': {'token': token},'msg': '登陆成功'})


@login_required
def logout():
    if hasattr(g, 'user'):
        logout_user(g.user)
    logout_user()
    return jsonify({'status': 1, 'data': {}, 'msg': '退出成功'})
