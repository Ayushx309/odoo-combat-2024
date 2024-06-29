from flask import Flask
from config import app
from datetime import timedelta

from src.py import index

if __name__ ==  "__main__":
    app.run(debug=True)