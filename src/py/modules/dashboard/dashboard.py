from flask import Flask,render_template,session,redirect,url_for
from config import app,cursor,conn
import json
import ast
from collections import namedtuple
from src.py.modules.extras.func import authentication

@app.route('/dashboard')
@authentication
def dashboard():
    activeUserData = session.get('activeUserData')
    papers = getAllPapers(activeUserData['id'])
    print(papers)
    return render_template('Dashboard/index.html',userName = activeUserData['user_name'],displayName = activeUserData['display_name'],role=activeUserData['role'],lastlogin=activeUserData['lastlogin'],papers=papers)

def getAllPapers(userid):
    query = '''
    SELECT 
        p.paper_id, p.paper_name, p.paper_desc, p.paper_path, 
        p.paper_password, p.paper_version, a.user_name AS paper_uploadedby, 
        p.paper_schedule_time, p.paper_expiry_time, p.paper_access, p.paper_timestamp
    FROM papers p
    JOIN accounts a ON p.paper_uploadedby = a.user_id
    '''
    cursor.execute(query)
    result = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    Paper = namedtuple('Paper', columns)
    papers = [Paper(*row) for row in result] if result else []
    accessible_papers = []
    for paper in papers:
        try:
            access_list = json.loads(paper.paper_access)
        except json.JSONDecodeError:
            access_list = []

        if userid in access_list:
            accessible_papers.append(paper)
    return accessible_papers