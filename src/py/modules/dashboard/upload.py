from flask import Flask,render_template,redirect,url_for,session,request
from src.py.modules.extras.func import authentication
from werkzeug.security import generate_password_hash
from mysql.connector import Error
from config import app,conn,cursor
import json

@app.route('/upload',methods=['POST','GET'])
@authentication
def upload():
    activeUserData = session.get('activeUserData')
    return render_template('dashboard/upload.html',userName = activeUserData['user_name'],displayName = activeUserData['display_name'])