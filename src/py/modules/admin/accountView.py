from flask import Flask,render_template,redirect,url_for,session
from src.py.modules.extras.func import authentication
from config import app
import json

@app.route('/admin/accounts/view',methods=['POST','GET'])
@authentication
def accountsView():
    activeUserData = session.get('activeUserData')
    return render_template('admin/accountView.html',userName = activeUserData['user_name'],displayName = activeUserData['display_name'])