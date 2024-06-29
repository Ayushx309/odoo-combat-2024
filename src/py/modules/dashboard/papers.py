from flask import Flask,render_template,session,redirect,url_for
from config import app,cursor,conn
import json
import ast
from collections import namedtuple
from src.py.modules.extras.func import authentication

@app.route('/paper/view')
@authentication
def paperView():
    activeUserData = session.get('activeUserData')
    return render_template('Dashboard/index.html',userName = activeUserData['user_name'],displayName = activeUserData['display_name'],role=activeUserData['role'],lastlogin=activeUserData['lastlogin'])