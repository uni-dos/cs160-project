from flask import Flask

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