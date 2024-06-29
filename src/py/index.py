from flask import Flask,render_template,session,redirect,url_for
from config import app,cursor,conn

@app.route('/index')
def index():
    return render_template('index.html')