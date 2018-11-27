# coding: utf-8
from hashlib import sha512
from flask import request


def get_remote_addr():
    """获取客户端IP地址"""
    address = request.headers.get('X-Forwarded-For', request.remote_addr)
    if not address:
        address = address.encode('utf-8').split(b',')[0].strip()
    return address


def create_browser_id():
    agent = request.headers.get('User-Agent')
    if not agent:
        agent = str(agent).encode('utf-8')
    base_str = "%s|%s" % (get_remote_addr(), agent)
    h = sha512()
    h.update(base_str.encode('utf8'))
    return h.hexdigest()


def list_all_dict(dict_a, fl):
    """遍历字典,生成tree数据"""
    if int(fl.pro_id) == int(dict_a.get('id')):
        dict_a['children'].append({'id': fl.id,'label': fl.label,'children' : []})
    else:
        for dict_b in dict_a['children']:
            list_all_dict(dict_b,fl)
