from flask import Flask,render_template,redirect,url_for,session,request,send_file
from src.py.modules.extras.func import authentication
from werkzeug.security import generate_password_hash
from mysql.connector import Error
from config import app,conn,cursor
import json
import secrets
import string
import PyPDF2
import os
import uuid
import time



@app.route('/upload',methods=['POST','GET'])
@authentication
def upload():
    activeUserData = session.get('activeUserData')
    if request.method == 'POST':

        paperData = {
            'name' : request.form.get('paper_name'),
            'description' : request.form.get('paper_desc'),
            'schedule_time' : request.form.get('paper_stime'),
            'expiry_time' : request.form.get('paper_etime'),
            'paper_access' : extractTagIds(request.form.get('tags')),
            'paperPDF' : request.files.get('paper_pdf'),
            'uploaded_by' : activeUserData.get("id")
        } 

        filePathAndPass = encryptPDFandSave(paperData.get("paperPDF"))
        paperData['path'] = filePathAndPass[0]
        paperData['pass'] = filePathAndPass[1]
        paperData['version'] = 1
        paperData['paper_access'] = '[' + ','.join(map(str,paperData['paper_access'] )) + ']'

        
        if addPaperToDB(paperData):
            session['message'] ="""
            <script>
            function showSuccessMessage() {
            Swal.fire({
                icon: 'success',
                title: 'Success!',
                text: 'Paper uploaded successfully!',
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
                text: 'Paper upload failed!',
                confirmButtonText: 'OK'
            });
            }
            showSuccessMessage();
            </script>
            """
          
        
        return redirect(url_for('upload'))
    message = session.pop('message', None)
    return render_template('dashboard/upload.html',userName = activeUserData['user_name'],displayName = activeUserData['display_name'],message=message)


def extractTagIds(tags_json):
    try:
        # Parse the JSON string into a Python list of dictionaries
        tags_list = json.loads(tags_json)
        
        # Extract the IDs from each tag in the tags_list
        tag_ids = [tag['id'] for tag in tags_list]
        
        return tag_ids
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return []
    except Exception as e:
        print(f"Error extracting tag IDs: {e}")
        return []


def encryptPDFandSave(pdf_file):
        pdf_file
        password = generateRandomPassword()
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        pdf_writer = PyPDF2.PdfFileWriter()
        for page_num in range(pdf_reader.numPages):
            pdf_writer.addPage(pdf_reader.getPage(page_num))

        pdf_writer.encrypt(password)

        save_directory = 'src/static/Storage/papers'

        os.makedirs(save_directory, exist_ok=True)
        uniqueFilename = generateUniqueFilename()

        encrypted_file_path = os.path.join(save_directory, uniqueFilename)
        storePath = f"/Storage/papers/{uniqueFilename}"

        with open(encrypted_file_path, 'wb') as encrypted_file:
            pdf_writer.write(encrypted_file)

        return [storePath,password]


def generateRandomPassword(length=12):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password

def generateUniqueFilename():
    unique_id = uuid.uuid4().hex[:8]
    timestamp = int(time.time())
    unique_filename = f'{timestamp}_{unique_id}.pdf'
    return unique_filename

def addPaperToDB(data: dict) -> bool:
    try:

        cursor.execute("INSERT INTO papers(paper_name, paper_desc, paper_path, paper_version, paper_uploadedby, paper_schedule_time, paper_expiry_time, paper_access, paper_password) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(data.get('name'),data.get('description'),data.get('path'),data.get('version'),data.get('uploaded_by'),data.get('schedule_time'),data.get('expiry_time'),data.get('paper_access'),data.get('pass'),))

        conn.commit()
        return True

    except Error as e:
        print(e)
        conn.rollback()
        return False
