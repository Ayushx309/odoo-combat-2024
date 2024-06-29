from flask import Flask,render_template,redirect,url_for,session,request
from src.py.modules.extras.func import authentication
from werkzeug.security import generate_password_hash
from mysql.connector import Error
from config import app,conn,cursor
import json

@app.route('/admin/accounts/create',methods=['POST','GET'])
@authentication
def accountsCreate():
    activeUserData = session.get('activeUserData')

    if request.method == 'POST':
        newUserData = {
            'username':request.form['user_name'],
            'display_name':request.form['user_dname'],
            'password':generate_password_hash(request.form['user_password'], method='scrypt'),
            'role':request.form.get('user_role')
        }  

        newUserDBStatus = addUserToDB(newUserData)
        if newUserDBStatus:
            session['message'] ="""
            <script>
            function showSuccessMessage() {
            Swal.fire({
                icon: 'success',
                title: 'Success!',
                text: 'Account created successfully!',
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
                text: 'Account creation failed!',
                confirmButtonText: 'OK'
            });
            }
            showSuccessMessage();
            </script>
            """
          
        
        return redirect(url_for('accountsCreate'))
    message = session.pop('message', None)
    return render_template('admin/accountCreate.html',userName = activeUserData['user_name'],displayName = activeUserData['display_name'], message=message)

def addUserToDB(data: dict)-> bool:
    try:
        cursor.execute("INSERT INTO accounts(user_name, user_dname, user_password, user_role) VALUES(%s,%s,%s,%s)",(data.get('username'),data.get('display_name'),data.get('password'),data.get('role'),))
        conn.commit()
        return True
    except Error as e:
        conn.rollback()
        return False