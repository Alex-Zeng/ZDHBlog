from flask import render_template, url_for, jsonify, request, session, redirect, make_response, Response, json, g, current_app
from main.models.index_model import User, Project, Request_api, File_level
from ext import db, login_manager, load_user, simple_cache
from flask_login import login_user, login_required, logout_user, current_user
from utils import create_browser_id,list_all_dict
from itsdangerous import URLSafeSerializer, BadData, constant_time_compare


@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({'status': 2, 'data': {'url': request.url}, 'msg': "未登录,请先登陆"})


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
    校验token
    这里的入参就是get_id()的返回值
    """
    return load_token(token)


def register(*args, **kwargs):
    """注册"""
    if request.method == 'POST':
        json_data = request.json
        telephone = json_data.get('telephone')  # 不开放注册,暂时只能自己用
        username = json_data.get('username')
        password1 = json_data.get('password1')
        password2 = json_data.get('password2')

        if User.query.filter(User.telephone == telephone).first():
            return jsonify({'status': '0', 'data': {}, 'msg': '该手机号码已被注册!'})

        if User.query.filter(User.username == username).first():
            return jsonify({'status': '0', 'data': {}, 'msg': '该用户名已被使用!'})

        if password1 != password2:
            return jsonify({'status': '0', 'data': {}, 'msg': '两次输入的密码不相同,请核对后再次提交!'})

        user1 = User(telephone=telephone, username=username, password=password1)
        db.session.add(user1)
        db.session.commit()
        return jsonify({'status': '1', 'data': {}, 'msg': '注册成功'})


def login(*args, **kwargs):
    if request.method == 'POST':
        json_data = request.json
        # telephone = request.form.get('telephone')
        username = json_data.get('username')
        password = json_data.get('password')
        user = User.query.filter(User.username == username).first()

        if not user:
            return jsonify({'status': 0, 'data': {}, 'msg': '用户不存在'})

        if not User.check_password(user, password):
            return jsonify({'status': 0, 'data': {}, 'msg': '用户密码错误,请重新输入'})

        login_user(user)  # 触发session机制，通过user.get_id()就可以获取到token
        g.user = user
        # 完成登录后将token存到缓存中并设置过期时间，后面校验时如果缓存中不存在，则报错
        life_time = current_app.config.get("TOKEN_LIFETIME")
        token = user.get_id(life_time)
        simple_cache.set(token, 1, timeout=life_time)  # 这样存数据,可以缓存多个token,  键值对 key 就是token,而不是value.
        return jsonify({'status': 1, 'data': {'token': token, 'userdata': {
            'username': user.username, 'role': user.role, 'userstatus': user.status
        }}, 'msg': '登陆成功'})


@login_required
def logout():
    if hasattr(g, 'user'):
        logout_user(g.user)
    logout_user()
    return jsonify({'status': 1, 'data': {}, 'msg': '退出成功'})


@login_required
def create_project():
    """创建项目"""
    if request.method == 'POST':
        json_data = request.json
        project_name = json_data.get('project_name')
        author_id = user_loader(session.get('user_id')).id

        if not project_name:
            return jsonify({'status': '0', 'data': {}, 'msg': '项目名不能为空'})

        if Project.query.filter(Project.name == project_name).first():
            return jsonify({'status': '0', 'data': {}, 'msg': '该项目名已被使用,请重新填写'})

        new_project = Project(name=project_name, author_id=author_id, env_id=1)
        db.session.add(new_project)
        db.session.commit()
        return jsonify({'status': 1, 'data': {}, 'msg': '创建项目成功'})


@login_required
def get_project_list():
    """获取项目列表"""
    if request.method == 'GET':
        user_id = user_loader(session.get('user_id')).id
        project_lists = list(Project.query.filter(Project.author_id == user_id).all())
        project_list = {}
        for project in project_lists:
            project_list[project.id] = project.name

        return jsonify({'status': 1, 'data': {'list': project_list}, 'msg': '请求项目列表成功'})


@login_required
def add_request_api():
    """添加接口"""
    if request.method == 'POST':
        json_data = request.json
        req_name = json_data.get('req_name')
        project_id = json_data.get('project_id')
        file_level_id = json_data.get('file_level_id')
        req_method = json_data.get('req_method')
        req_url = json_data.get('req_url')
        req_data = json_data.get('req_data')

        if not req_method or not req_url or not req_data or not req_name:
            return jsonify({'status': '0', 'data': {}, 'msg': '请求名,方法,URL,数据不能为空'})

        if Request_api.query.filter(Request_api.req_name == req_name).first():
            return jsonify({'status': '0', 'data': {}, 'msg': '该接口名已被使用,请重新填写'})

        new_api = Request_api(req_name=req_name, project_id=project_id, req_method=req_method, req_url=req_url, req_data=req_data)
        db.session.add(new_api)
        db.session.commit()
        return jsonify({'status': 1, 'data': {}, 'msg': '添加接口成功'})


@login_required
def get_api_list():
    """获取接口列表"""
    if request.method == 'get':
        json_data = request.json
        project_id = json_data.get('project_id')

        api_list = list(Request_api.query.filter(Request_api.project_id == project_id).all())

        return jsonify({'status': 1, 'data': {'list': api_list}, 'msg': '请求接口列表成功'})

@login_required
def add_file_level():
    """添加文件夹"""
    if request.method == 'POST':
        json_data = request.json
        project_id = json_data.get('project_id')
        pro_id = json_data.get('pro_id')
        label = json_data.get('label')
        current_id = json_data.get('current_id')

        if not project_id or not label:
            return jsonify({'status': '0', 'data': {}, 'msg': '不能为空'})
        if not current_id:
            # 添加新数据
            fl = File_level(project_id=project_id,pro_id=pro_id,label=label)
            db.session.add(fl)
            db.session.commit()
            return jsonify({'status': '1', 'data': {}, 'msg': '添加成功'})
        else:
            # 更新数据
            fl1 = File_level.query.filter(File_level.id == current_id).first()
            if not fl1:
                return jsonify({'status': '0', 'data': {}, 'msg': '没有这条数据'})
            fl1.label = label
            db.session.commit()
            return jsonify({'status': '1', 'data': {}, 'msg': '更新列表成功'})


def get_file_level():
    """获取文件夹"""
    if request.method == 'GET':
        json_data = request.args
        project_id = json_data.get('project_id')
        fl_datas=[]
        fls = File_level.query.filter(File_level.project_id == project_id).order_by('id').all()

        if fls:
            for fl in fls:
                fl_data = {}
                if  int(fl.pro_id) == 0:
                    fl_data['id'] = fl.id
                    fl_data['label'] = fl.label
                    fl_data['children'] = []
                    fl_datas.append(fl_data)

                for da in fl_datas:
                    if  int(fl.pro_id) > 0:
                        list_all_dict(da,fl)

        return jsonify({'status': '1', 'data': fl_datas, 'msg': '成功'})


def delete_file_level():
    """删除文件夹"""
    if request.method == 'GET':
        json_data = request.args
        id = json_data.get('file_id')
        fls = File_level.query.filter(File_level.id == id and File_level.pro_id == id).all()

        db.session.delete(fls)

        return jsonify({'status': '1', 'data': {}, 'msg': '删除成功'})
