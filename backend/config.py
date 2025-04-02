import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB_URL = os.getenv('DB_URL')
DB_PORT = int(os.getenv('DB_PORT'))
DB_UNAME = os.getenv('DB_UNAME')
DB_PSWD = os.getenv('DB_PSWD')
DB_NAME = os.getenv('DB_NAME')
db_uri = f"mysql+pymysql://{DB_UNAME}:{DB_PSWD}@{DB_URL}:{DB_PORT}/{DB_NAME}"

app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)