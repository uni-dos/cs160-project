from flask import Flask
import mysql.connector
import os

# connect to DB
db_connection = mysql.connector.connect(
    host = os.get('DB_URL'),
    user = os.get('DB_UNAME'),
    password = os.get('DB_PSWD'),
    database = os.get('DB_NAME')
)

app = Flask(__name__)

@app.route('/')
def helloworld():
    return 'Hello World'

@app.route('/login')
def login():
    return True

@app.route('/signup')
def signup():
    return True


if __name__ == '__main__' :
    app.run()
    db_connection.close()