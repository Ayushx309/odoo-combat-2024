from flask import Flask, request, jsonify,session
import random
import re
from config import app,conn,cursor
from mysql.connector import Error
from werkzeug.security import check_password_hash
import os


@app.route('/api/checkUsernameAvailability', methods=['POST'])
def checkUsernameAvailability():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    data = request.get_json()
    
    if not data or 'username' not in data:
        return jsonify({'error': 'Please provide a username'}), 400
    
    username: str = data['username']
    print(checkUsernameAvailabilityDB(username))
    return jsonify({'exists': checkUsernameAvailabilityDB(username)}), 200


@app.route('/api/accounts', methods=['POST'])
def getaccounts():
    try:
        cursor.execute("SELECT * FROM accounts")
        accounts = cursor.fetchall()

        response_data = {
                'accounts': [{
                    'username': account[1], 'display_name': account[2], 'role': account[4], 
                    'last_login': account[5], 'creation' : account[6], 'id' : account[0]
                } for account in accounts]
            }
        
        return jsonify(response_data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/deleteAccount', methods=['POST'])
def delete_account():
    user_id = request.json.get('id')
    if user_id:
        deleteStatus = deleteAccount(user_id)
        if deleteStatus:
            return jsonify({"status": "success", "message": "Account deleted successfully"}), 200
        else:
            return jsonify({"status": "failure", "message": "Account not deleted!"}), 500
    else:
        return jsonify({"status": "error", "message": "Account not found"}), 404


def checkUsernameAvailabilityDB(username):
    cursor.execute("SELECT * FROM accounts WHERE user_name = %s",(username,))
    result: tuple = cursor.fetchone()
    if result:
       return True
    else:
       return False
    
def deleteAccount(id):
    try:
        cursor.execute("DELETE FROM accounts WHERE user_id = %s", (id,))
        if cursor.rowcount > 0:
            return True
        else:
            return False
    except Exception as e:
        return False