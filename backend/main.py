from flask import request, jsonify
from config import app, db
from models import User, Follow
from bcrypt import hashpw, checkpw, gensalt
from sqlalchemy import text


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
        return jsonify({"message": "Incorrect username or password"}), 404
    
    # compare password to the hashed password
    if checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        # return username to frontend
        return jsonify({"username": username}), 201
    else:
        return jsonify({"message": "Incorrect username or password"}), 401


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
    
    try:
        # check if username already exists
        user = User.query.filter_by(username=username).first()
        if user:
            return jsonify({"taken": True, "message": "Username already taken"}), 404
        # store User in db
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 400
    
    # return username to frontend
    return jsonify({"username": username}), 201


@app.route("/follow", methods=["POST"])
def follow():
    follower = request.json.get("follower")
    followee = request.json.get("followee")

    if not follower or not followee or follower == followee:
        return jsonify({"message": "Invalid data"}), 400

    try:
        # store Follow in db
        new_follow = Follow(username_follower=follower, username_followee=followee)
        db.session.add(new_follow)
        db.session.commit()
        # return follower and followee to frontend
        return jsonify({"follower": follower, "followee": followee}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 400


@app.route("/unfollow", methods=["DELETE"])
def unfollow():
    follower = request.json.get("follower")
    followee = request.json.get("followee")

    if not follower or not followee:
        return jsonify({"message": "Invalid data"}), 400
    
    try:
        # delete Follow in db
        sql = text("DELETE FROM follow WHERE username_follower = :follower AND username_followee = :followee")
        db.session.execute(sql, {"follower": follower, "followee": followee})
        db.session.commit()
        # return follower and followee to frontend
        return jsonify({"follower": follower, "followee": followee}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 400


@app.route("/<username>/following", methods=["GET"])
def get_following(username):
    if not username:
        return jsonify({"message": "Invalid data"}), 400
    
    try:
        # query to find the usernames the user is following
        sql = text("SELECT username_followee FROM follow WHERE username_follower = :username")
        result = db.session.execute(sql, {"username": username})
        # convert the result to an array of usernames
        following = [row.username_followee for row in result]
        # return the username and following array to frontend
        return jsonify({"username": username, "following": following}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@app.route("/<username>/followers", methods=["GET"])
def get_followers(username):
    if not username:
        return jsonify({"message": "Invalid data"}), 400
    
    try:
        # query to find the usernames that are following the user
        sql = text("SELECT username_follower FROM follow WHERE username_followee = :username")
        result = db.session.execute(sql, {"username": username})
        # convert the result to an array of usernames
        followers = [row.username_follower for row in result]
        # return the username and follower array to frontend
        return jsonify({"username": username, "followers": followers}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)