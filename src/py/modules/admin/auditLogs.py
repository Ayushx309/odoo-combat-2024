from flask import Flask,render_template,redirect,url_for,session,request
from src.py.modules.extras.func import authentication
from werkzeug.security import generate_password_hash
from mysql.connector import Error
from config import app,conn,cursor
import json

@app.route('/admin/auditLogs/login',methods=['POST','GET'])
@authentication
def auditLogs():
    activeUserData = session.get('activeUserData')
    if activeUserData['role'] not in ['administrator']:
        return redirect(url_for('dashboard'))
    loginLogs = getLoginLogs()
    print(loginLogs)
    return render_template('admin/auditLogsLogin.html',userName = activeUserData['user_name'],displayName = activeUserData['display_name'],role=activeUserData['role'],lastlogin=activeUserData['lastlogin'],loginLogs=loginLogs)


@app.route('/admin/auditLogs/papers',methods=['POST','GET'])
@authentication
def auditLogs2():
    activeUserData = session.get('activeUserData')
    if activeUserData['role'] not in ['administrator']:
        return redirect(url_for('dashboard'))
    return render_template('admin/auditLogsPapers.html',userName = activeUserData['user_name'],displayName = activeUserData['display_name'],role=activeUserData['role'],lastlogin=activeUserData['lastlogin'])



def getLoginLogs():
    cursor.execute('''
    SELECT 
        accounts.user_name, 
        audit.audit_ip, 
        audit.audit_timestamp 
    FROM audit 
    JOIN accounts ON audit.user_id = accounts.user_id 
    WHERE audit.audit_type = "login"
    ''')
    result = cursor.fetchall()
    return result
    