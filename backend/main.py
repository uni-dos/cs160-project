from flask import request, jsonify
from config import app, db
from models import User, Recipe, Follow  # import all used models
from bcrypt import hashpw, checkpw, gensalt
from sqlalchemy import text, select

@app.route("/")
def home():
    return "✅ Flask is running!"

# Login
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    if not username or not password:
        return jsonify({"message": "No username"}), 400
    
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"message": "Incorrect username or password"}), 404
    
    if checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        return jsonify({"username": username}), 201
    else:
        return jsonify({"message": "Incorrect username or password"}), 401

# Signup
@app.route("/signup", methods=["POST"])
def signup():
    username = request.json.get("username")
    password = request.json.get("password")

    if not username or not password:
        return jsonify({"message": "No username or password"}), 400
    
    hashed_password = hashpw(password.encode("utf-8"), gensalt())

    try:
        user = User.query.filter_by(username=username).first()
        if user:
            return jsonify({"taken": True, "message": "Username already taken"}), 404

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 400

    return jsonify({"username": username}), 201

# Create Recipe
@app.route("/recipe", methods=["POST"])
def create_recipe():
    data = request.get_json()
    
    title = data.get("title")
    short_description = data.get("short_description")
    steps = data.get("steps")
    time = data.get("time")
    servings = data.get("servings")
    author_username = data.get("author_username")

    if not (title and steps and author_username):
        return jsonify({"message": "Missing required fields"}), 400

    new_recipe = Recipe(
        title=title,
        short_description=short_description,
        steps=steps,
        time=time,
        servings=servings,
        author_username=author_username,
        sustainability_rating=0,
        average_rating=0
    )

    try:
        db.session.add(new_recipe)
        db.session.commit()
        return jsonify({"message": "Recipe created!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Retrieve Recipes
@app.route("/recipe", methods=["GET"])
def get_recipes():
    recipes = Recipe.query.all()
    if not recipes:
        return jsonify({"message" : "No recipes"}), 303 # 303 meaning there is nothing
    recipes_list = []
    for recipe in recipes:
        recipes_list.append(recipe.to_json())
    return jsonify({"recipes" : recipes_list}), 201

# Follow
@app.route("/follow", methods=["POST"])
def follow():
    follower = request.json.get("follower")
    followee = request.json.get("followee")

    if not follower or not followee or follower == followee:
        return jsonify({"message": "Invalid data"}), 400

    try:
        new_follow = Follow(username_follower=follower, username_followee=followee)
        db.session.add(new_follow)
        db.session.commit()
        return jsonify({"follower": follower, "followee": followee}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 400

# Unfollow
@app.route("/unfollow", methods=["DELETE"])
def unfollow():
    follower = request.json.get("follower")
    followee = request.json.get("followee")

    if not follower or not followee:
        return jsonify({"message": "Invalid data"}), 400
    
    try:
        sql = text("DELETE FROM follow WHERE username_follower = :follower AND username_followee = :followee")
        db.session.execute(sql, {"follower": follower, "followee": followee})
        db.session.commit()
        return jsonify({"follower": follower, "followee": followee}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 400

# Get following list
@app.route("/<username>/following", methods=["GET"])
def get_following(username):
    if not username:
        return jsonify({"message": "Invalid data"}), 400
    
    try:
        sql = text("SELECT username_followee FROM follow WHERE username_follower = :username")
        result = db.session.execute(sql, {"username": username})
        following = [row.username_followee for row in result]
        return jsonify({"username": username, "following": following}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

# Get followers list
@app.route("/<username>/followers", methods=["GET"])
def get_followers(username):
    if not username:
        return jsonify({"message": "Invalid data"}), 400
    
    try:
        sql = text("SELECT username_follower FROM follow WHERE username_followee = :username")
        result = db.session.execute(sql, {"username": username})
        followers = [row.username_follower for row in result]
        return jsonify({"username": username, "followers": followers}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)
