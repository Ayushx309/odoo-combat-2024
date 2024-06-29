from flask import Flask
import mysql.connector

def odooCombat2024():
    app = Flask(__name__, template_folder='./src/templates', static_folder='./src/static')
    app.secret_key = 'odooCombat2024'

    return app
app = odooCombat2024()


db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'SPDS',
    'auth_plugin': ''
}
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()