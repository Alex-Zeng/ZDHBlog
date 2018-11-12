from flask import render_template, url_for, jsonify


def index():
    return render_template('index.html')


def foo():
    url_for('.foo')
    return url_for('admin.foo')

def json_str():
    return jsonify({'name':"李太白",'words':"十步杀一人，千里不留行。"})
