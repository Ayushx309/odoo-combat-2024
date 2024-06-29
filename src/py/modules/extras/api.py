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
    
    username = data['username']
    print(checkUsernameAvailabilityDB(username))
    return jsonify({'exists': checkUsernameAvailabilityDB(username)}), 200


def checkUsernameAvailabilityDB(username):
    cursor.execute("SELECT * FROM accounts WHERE user_name = %s",(username,))
    result: tuple = cursor.fetchone()
    if result:
       return True
    else:
       return False