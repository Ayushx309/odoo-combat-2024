from flask import Flask,render_template,session,request,redirect,url_for
from config import app,conn,cursor
from werkzeug.security import check_password_hash
from collections import namedtuple





@app.route('/auth/login',methods=['POST','GET'])
def login():

   if 'activeUserData' in session:
      return redirect(url_for('dashboard'))

   if request.method == 'POST':
      username = request.form['username']
      password = request.form['password']
      username = username.strip()


      if doesUserExist(username):
         if check_password_hash(getUserPassword(username),password):
            session.permanent = True 
            userAccountData: tuple = fetchUserData(username)
            session['activeUserData'] = { 
               "id": userAccountData.user_id,
               "user_name" : userAccountData.user_name,
               "display_name" : userAccountData.user_dname,
               "role":userAccountData.user_role,
               "lastlogin":userAccountData.user_lastlogin
            }

            return redirect(url_for('dashboard'))
         else:
            return render_template('login/login.html',loginError="Password Incorrect!")  
      else:
         return render_template('login/login.html',loginError="Username Invalid!")


   return render_template('login/login.html')


@app.route('/')
def root():
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


def doesUserExist(username):

   cursor.execute("SELECT * FROM accounts WHERE user_name = %s",(username,))
   result: tuple = cursor.fetchone()

   if result:
      return True
   else:
      return False
   
def getUserPassword(username):

   cursor.execute("SELECT user_password FROM accounts WHERE user_name = %s",(username,))
   result: str = cursor.fetchone()[0]
   return result


def fetchUserData(username):

   cursor.execute('SELECT * FROM accounts WHERE user_name = %s',(username,))
   result = cursor.fetchone()
   columns = cursor.column_names
   User = namedtuple('User', columns)
   if result:
      user = User(*result)
      return user  
   return None




