from flask import render_template,url_for

def index():
    return  render_template('index.html')

def foo():
    url_for('.foo')
    return url_for('index.foo')