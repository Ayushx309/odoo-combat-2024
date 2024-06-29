from flask import Flask,render_template,session,redirect,url_for,request
from config import app,cursor,conn
from collections import namedtuple
from src.py.modules.extras.func import authentication
import json
import ast
import datetime

@app.route('/paper/view')
@authentication
def paperView():
    activeUserData = session.get('activeUserData')
    if request.method == 'GET':
        if request.args.get('id') and doesUserHasAccess(activeUserData['id'],request.args.get('id')):
                paperData,isWithinTimeBool = getPaperData(request.args.get('id'))
        else:
            return redirect(url_for('dashboard'))


    return render_template('Dashboard/paperView.html',userName = activeUserData['user_name'],displayName = activeUserData['display_name'],role=activeUserData['role'],lastlogin=activeUserData['lastlogin'], paperData = paperData,isWithinTimeBool=isWithinTimeBool)

def doesUserHasAccess(userID,paperID):
    try:
        cursor.execute("SELECT paper_access FROM papers WHERE paper_id = %s",(paperID,))
        result = cursor.fetchone()[0]
        try:
            access_list = json.loads(result)
        except json.JSONDecodeError:
            access_list = []

        if userID in access_list:
            return True
        else:
            return False
    except Exception as e:
        print(e)

def getPaperData(id):
    try:
        cursor.execute("SELECT * FROM papers WHERE paper_id = %s",(id,))
        result = cursor.fetchone()
        columns = cursor.column_names
        Paper = namedtuple('Paper', columns)
        if result:
            paper = Paper(*result)
            if isWithinSchedule(paper.paper_schedule_time,paper.paper_expiry_time):
                return paper,True
            else:
                return paper,False
        return None
    except Exception as e:
        print(e)

def isWithinSchedule(paper_schedule_time, paper_expiry_time):
    current_time = datetime.datetime.now()
    return paper_schedule_time <= current_time <= paper_expiry_time
