from flask import Flask,render_template,redirect,url_for,session,request
from src.py.modules.extras.func import authentication
from werkzeug.security import generate_password_hash
from config import app,conn,cursor
from config import app
from collections import namedtuple
from mysql.connector import Error
import json

@app.route('/admin/accounts/edit',methods=['POST','GET'])
@authentication
def accountsEdit():
    global user_id
    if request.method == 'GET':
        if request.args.get('id') and doesUserExist(request.args.get('id')):
            user_id = request.args.get('id')
            userData = fetchUserData(user_id)
        else:
            return redirect(url_for('accountsView'))
    activeUserData = session.get('activeUserData')
    if activeUserData['role'] not in ['administrator']:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        editUserData = {
            'username':request.form['user_name'],
            'display_name':request.form['user_dname'],
            'password':generate_password_hash(request.form['user_password'], method='scrypt'),
            'role':request.form.get('user_role')
        }  

        editUserDBStatus = editUserDataDB(editUserData,user_id)
        if editUserDBStatus:
            session['message'] ="""
            <script>
            function showSuccessMessage() {
            Swal.fire({
                icon: 'success',
                title: 'Success!',
                text: 'Account edited successfully!',
                confirmButtonText: 'OK'
            });
            }
            showSuccessMessage();
            </script>"""
                
            
        else:
            session['message'] = """
            <script>
            function showSuccessMessage() {
            Swal.fire({
                icon: 'error',
                title: 'Failed!',
                text: 'Account editing failed!',
                confirmButtonText: 'OK'
            });
            }
            showSuccessMessage();
            </script>
            """
          
        
        return redirect(url_for('accountsEdit'))
    message = session.pop('message', None)
    return render_template('admin/accountEdit.html',userName = activeUserData['user_name'],displayName = activeUserData['display_name'],userData=userData,message=message,role=activeUserData['role'],lastlogin=activeUserData['lastlogin'])

def doesUserExist(userid):
   cursor.execute("SELECT * FROM accounts WHERE user_id = %s",(userid,))
   result: tuple = cursor.fetchone()
   if result:
      return True
   else:
      return False

def fetchUserData(userid):
   cursor.execute('SELECT * FROM accounts WHERE user_id = %s',(userid,))
   result = cursor.fetchone()
   columns = cursor.column_names
   User = namedtuple('User', columns)
   if result:
      user = User(*result)
      return user  
   return None


def editUserDataDB(data: dict,id)-> bool:
    try:
        cursor.execute("UPDATE accounts SET user_name=%s, user_dname=%s, user_password=%s, user_role=%s WHERE user_id=%s",(data.get('username'),data.get('display_name'),data.get('password'),data.get('role'),id,))
        conn.commit()
        return True
    except Error as e:
        conn.rollback()
        return False