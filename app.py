from flask import Flask
from config import app
from datetime import timedelta
from src.py.modules.dashboard import dashboard,upload,papers
from src.py.modules.login import login
from src.py.modules.admin import accountCreate,accountEdit,accountView
from src.py.modules.extras import api

if __name__ ==  "__main__":
    app.run(debug=True)