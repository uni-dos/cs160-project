from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB_URL = "localhost"
DB_PORT = 3306
DB_UNAME = "root"
DB_PSWD = "123456"
DB_NAME = "cs160_project_db"

db_uri = f"mysql+pymysql://{DB_UNAME}:{DB_PSWD}@{DB_URL}:{DB_PORT}/{DB_NAME}"
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
