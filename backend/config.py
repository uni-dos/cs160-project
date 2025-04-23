import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_session import Session
 
app = Flask(__name__)
CORS(app, supports_credentials=True)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret=os.getenv('TOKEN_KEY')
Session(app)
 
DB_URL = os.getenv('DB_URL')
DB_PORT = int(os.getenv('DB_PORT'))
DB_UNAME = os.getenv('DB_UNAME')
DB_PSWD = os.getenv('DB_PSWD')
DB_NAME = os.getenv('DB_NAME')
db_uri = f"mysql+pymysql://{DB_UNAME}:{DB_PSWD}@{DB_URL}:{DB_PORT}/{DB_NAME}"
 
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
 
db = SQLAlchemy(app)