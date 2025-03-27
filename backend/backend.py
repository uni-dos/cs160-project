from flask import Flask, request, jsonify
import mysql.connector
import os


def getDBConnection() :
    
    return mysql.connector.connect(
        host = os.get('DB_URL'),
        user = os.get('DB_UNAME'),
        password = os.get('DB_PSWD'),
        database = os.get('DB_NAME')
)

app = Flask(__name__)

# not sure if needed
@app.route('/')
def helloworld():
    return 'Hello World'

@app.route('/login', methods=['POST'])
def login():
    # in here we add the user to the db
    # hash the password and create a uid
    # uid will be the index and will be part of the 

    # simple test for now
    username = request.form.get('username')
    password = request.form.get('password')

    if username != '' or password != '' :
        print('username is ' + username)
        return jsonify({"message" : "Welcome"}), 200

    # return 309 if user exists
    return jsonify({"message" : "user already exists"}), 309

@app.route('/signup', methods=['POST'])
def signup():
     # in here we add the user to the db
    # hash the password and create a uid
    # uid will be the index and will be part of the 

    # simple test for now
    username = request.form.get('username')
    password = request.form.get('password')

    if username != '' or password != '' :
        print('username is ' + username)
        return jsonify({"message" : "Welcome"}), 200

    # return 309 if user exists
    return jsonify({"message" : "user already exists"}), 309

# get posts
@app.route('/post',  methods=['GET'])
def post() :
    return True

# create post
@app.route('/post',  methods=['POST'])
def post() :
    return True

# delete post
@app.route('/post',  methods=['DELETE'])
def post() :
    return True

if __name__ == '__main__' :
    app.run()