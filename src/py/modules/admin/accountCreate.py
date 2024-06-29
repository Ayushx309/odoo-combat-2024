from flask import Flask,render_template,redirect,url_for,session
from src.py.modules.extras.func import authentication
from config import app
import json

@app.route('/admin/accounts/create',methods=['POST','GET'])
@authentication
def accountsCreate():
    activeUserData = session.get('activeUserData')
    return render_template('admin/accountCreate.html',userName = activeUserData['user_name'],displayName = activeUserData['display_name'])