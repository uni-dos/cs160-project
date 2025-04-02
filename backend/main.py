from flask import request, jsonify
from config import app, db
from models import User
from bcrypt import hashpw, checkpw, gensalt


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    if not username or not password:
        return (
            jsonify({"message": "No username"}),
            400
        )
    
    # get User from db
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"message": "Username not found"}), 404
    
    # compare password to the hashed password
    if checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        # return username to frontend
        return jsonify({"username": username}), 201
    else:
        return jsonify({"message": "Incorrect password"}), 401


@app.route("/signup", methods=["POST"])
def signup():
    username = request.json.get("username")
    password = request.json.get("password")

    if not username or not password:
        return (
            jsonify({"message": "No username or password"}),
            400
        )
    
    # generate hashed password
    hashed_password = hashpw(password.encode("utf-8"), gensalt())
    
    # store User in db
    new_user = User(username=username, password=hashed_password)
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
    # return username to frontend
    return jsonify({"username": username}), 201


if __name__ == "__main__":
    app.run(debug=True)