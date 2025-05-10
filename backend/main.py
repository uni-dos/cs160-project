from flask import request, jsonify, session
from flask_session import Session
from config import app, db
from models import User, Recipe, Follow  # import all used models
from bcrypt import hashpw, checkpw, gensalt
from sqlalchemy import text, select
from datetime import datetime

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
    
    username = username.lower()
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"message": "Incorrect username or password"}), 404
    
    if checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        session["name"] = username
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
    
    username = username.lower()
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
    session['name'] = username
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
    ingredients = data.get("ingredients")

    if not (title and short_description and steps and time and servings and author_username and ingredients):
        return jsonify({"message": "Missing required fields"}), 400
    
    time = time["hours"] * 60 + time["mins"] # convert time to total minutes
    publish_date = datetime.now()
    
    total_sustainability_score = 0 # in grams of CO2 equivalent per serving

    def convert_to_grams(amount, unit, density=1.0):
        conversion_rates = {
            # weight based conversions
            "g": 1,
            "kg": 1000,
            "lb": 453.592,
            "oz": 28.3495,

            # volume based conversions
            "l": 1000 * density,
            "ml": 1 * density,
            "tbsp": 15 * density,
            "tsp": 5 * density,
            "cup": 240 * density,
            "pt": 473.176 * density,
            "qt": 946.353 * density,
            "gal": 3785.41 * density,
            "floz": 29.5735 * density,

            "qty": 100
        }
        return amount * conversion_rates.get(unit, 1)

    try:
        recipe_insert = text("""
                             INSERT INTO recipe (author_username, publish_date, title, short_description, steps, time, servings)
                             VALUES (:author_username, :publish_date, :title, :short_description, :steps, :time, :servings)
                             """)
        result = db.session.execute(recipe_insert, {"author_username": author_username, "publish_date": publish_date, "title": title, "short_description": short_description,
                                           "steps": steps, "time": time, "servings": servings})
        
        recipe_id = result.lastrowid
        
        contains_ingredient_insert = text("""
                                          INSERT INTO contains_ingredient (recipe_id, ingredient_name, amount, weight)
                                          VALUES (:recipe_id, :ingredient_name, :amount, :weight)
                                          """)

        for ingredient in ingredients:
            ingredient_name = ingredient["ingredient_name"]
            amount = ingredient["amount"]
            weight = ingredient["weight"]

            sustainability_query = text("""
                                        SELECT sustainability_score FROM ingredient
                                        WHERE ingredient_name = :ingredient_name
                                        """)
            sustainability_result = db.session.execute(sustainability_query, {"ingredient_name": ingredient_name}).fetchone()

            if sustainability_result:
                score_per_gram = sustainability_result[0]
                # need to convert the score (grams) to the ingredients weight
                weight_in_grams = convert_to_grams(amount, weight)
                ingredient_score = score_per_gram * weight_in_grams
                total_sustainability_score += ingredient_score

                db.session.execute(contains_ingredient_insert, {"recipe_id": recipe_id, "ingredient_name": ingredient_name, "amount": amount, "weight": weight})
            else:
                return jsonify({"message": f"Sustainability score does not exist for ingredient: {ingredient_name}"}), 400
        
        recipe_update = text("""
                             UPDATE recipe
                             SET sustainability_rating = :sustainability_rating
                             WHERE recipe_id = :recipe_id
                             """)
        # divide the total sustainability score by 1000 to get it in kg CO2
        db.session.execute(recipe_update, {"sustainability_rating": round(total_sustainability_score / 1000, 2), "recipe_id": recipe_id})
        
        db.session.commit()
        return jsonify({"message": "Recipe created!", "recipe_id": recipe_id, "sustainability_rating": total_sustainability_score}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Get all recipes
@app.route("/recipes", methods=["GET"])
def get_all_recipes():
    if not session.get('name'):
        return jsonify({"messege" : "not logged in"}), 401
    try:
        sql = text("""
                   SELECT r.recipe_id, r.author_username, r.publish_date, r.title, r.short_description, r.steps, r.time, r.servings, r.sustainability_rating, r.average_rating, i.ingredient_name, i.amount, i.weight
                   FROM recipe AS r
                   JOIN contains_ingredient as i
                   ON r.recipe_id = i.recipe_id
                   ORDER BY r.recipe_id DESC
                   """)
        
        result = db.session.execute(sql).fetchall()

        # convert Row objects to dictionaries
        rows = [row._mapping for row in result]

        recipes_dict = recipes_to_dict(rows)

        recipes_list = list(recipes_dict.values())
        return jsonify(recipes_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get user details (info and recipes)
@app.route("/user/<username>", methods=["GET"])
def get_user_details(username):
    try:
        user_query = text("""
                           SELECT password, bio
                           FROM user
                           WHERE user.username = :username
                           """)
        
        user_result = db.session.execute(user_query, {"username": username}).fetchone()
        hashed_password, bio = user_result

        recipes_query = text("""
                             SELECT r.recipe_id, r.author_username, r.publish_date, r.title, r.short_description, r.steps, r.time, r.servings, r.sustainability_rating, r.average_rating, i.ingredient_name, i.amount, i.weight
                             FROM recipe AS r
                             JOIN contains_ingredient as i
                             ON r.recipe_id = i.recipe_id
                             WHERE r.author_username = :username
                             ORDER BY r.recipe_id DESC
                             """)
        
        recipes_result = db.session.execute(recipes_query, {"username": username}).fetchall()
        # convert Row objects to dictionaries
        recipe_rows = [row._mapping for row in recipes_result]

        recipes_dict = recipes_to_dict(recipe_rows)
        recipes_list = list(recipes_dict.values())
        return jsonify({"username": username, "password": hashed_password, "bio": bio, "recipes": recipes_list}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


#rate (recipe title and user to find recipe then insert the rate and return the updated average rating that is triggered)
@app.route("/rate", methods=["POST"])
def rate_recipe():
    data = request.get_json()
    recipe_id = data.get("recipe_id")
    username = data.get("username")
    value = data.get("value")

    if not (recipe_id and username and value):
        return jsonify({"message": "Missing fields"}), 400

    if not (1 <= value <= 10):
        return jsonify({"message": "Rating must be between 1 and 10"}), 400

    try:
        # Check if user already rated this recipe
        existing_rating = db.session.execute(
            text("SELECT * FROM rate WHERE recipe_id = :recipe_id AND username = :username"),
            {"recipe_id": recipe_id, "username": username}
        ).fetchone()

        if existing_rating:
            return jsonify({"message": "You already rated this recipe"}), 400

        # Insert the new rating
        sql = text("""
            INSERT INTO rate (recipe_id, username, value)
            VALUES (:recipe_id, :username, :value)
        """)
        db.session.execute(sql, {"recipe_id": recipe_id, "username": username, "value": value})

        # Update the average rating of the recipe
        avg_sql = text("""
            UPDATE recipe
            SET average_rating = (
                SELECT AVG(value)
                FROM rate
                WHERE recipe_id = :recipe_id
            )
            WHERE recipe_id = :recipe_id
        """)
        db.session.execute(avg_sql, {"recipe_id": recipe_id})

        db.session.commit()
        return jsonify({"message": "Rating submitted"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    

#likes
@app.route("/like", methods=["POST"])
def like_recipe():
    data = request.get_json()
    recipe_id = data.get("recipe_id")
    username = data.get("username")

    if not (recipe_id and username):
        return jsonify({"message": "Missing fields"}), 400

    try:
        sql = text("""
            INSERT INTO likes (recipe_id, username)
            VALUES (:recipe_id, :username)
        """)
        db.session.execute(sql, {"recipe_id": recipe_id, "username": username})
        db.session.commit()
        return jsonify({"message": "Recipe liked!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

#unlike
@app.route("/unlike", methods=["DELETE"])
def unlike_recipe():
    data = request.get_json()
    recipe_id = data.get("recipe_id")
    username = data.get("username")

    if not (recipe_id and username):
        return jsonify({"message": "Missing fields"}), 400

    try:
        sql = text("""
            DELETE FROM likes
            WHERE recipe_id = :recipe_id AND username = :username
        """)
        db.session.execute(sql, {"recipe_id": recipe_id, "username": username})
        db.session.commit()
        return jsonify({"message": "Like removed"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
# get num likes
@app.route("/get-num-likes/<recipe_id>", methods=["GET"])
def get_num_likes(recipe_id):
    try:
        sql = text("SELECT COUNT(*) FROM likes WHERE recipe_id = :recipe_id")
        num_likes = db.session.execute(sql, {"recipe_id": recipe_id}).scalar()
        return jsonify({"recipe_id": recipe_id, "num_likes": num_likes}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# get liked recipes
@app.route("/get-likes/<username>", methods=["GET"])
def get_likes(username):
    if not username:
        return jsonify({"message": "Missing fields"}), 400
    
    try:
        sql = text("""
                    SELECT recipe.*
                    FROM recipe
                    JOIN likes ON recipe.recipe_id = likes.recipe_id
                    WHERE likes.username = :username
                   """)
        result = db.session.execute(sql, {"username": username})
        likes = [
            {
                "recipe_id": row.recipe_id,
                "author_username": row.author_username,
                "publish_date": row.publish_date,
                "title": row.title,
                "short_description": row.short_description,
                "steps": row.steps,
                "time": row.time,
                "servings": row.servings,
                "sustainability_rating": row.sustainability_rating,
                "average_rating": row.average_rating
            }
            for row in result
        ]
        return jsonify({"username": username, "likes": likes}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# create bookmark
@app.route("/bookmark", methods=["POST"])
def bookmark():
    recipe_id = request.json.get("recipe_id")
    username = request.json.get("username")

    if not (recipe_id or username):
        return jsonify({"message": "Missing fields"}), 400
    
    try:
        sql = text("""
                    INSERT INTO bookmark (recipe_id, username)
                    VALUES (:recipe_id, :username)
                   """)
        db.session.execute(sql, {"recipe_id": recipe_id, "username": username})
        db.session.commit()
        return jsonify({"recipe_id": recipe_id, "username": username}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 400

# unbookmark
@app.route("/unbookmark", methods=["DELETE"])
def unbookmark():
    recipe_id = request.json.get("recipe_id")
    username = request.json.get("username")

    if not (recipe_id or username):
        return jsonify({"message": "Missing fields"}), 400
    
    try:
        sql = text("""
                    DELETE FROM bookmark
                    WHERE recipe_id = :recipe_id AND username = :username
                   """)
        db.session.execute(sql, {"recipe_id": recipe_id, "username": username})
        db.session.commit()
        return jsonify({"recipe_id": recipe_id, "username": username}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 400

# get bookmarked recipes
@app.route("/get-bookmarks/<username>", methods=["GET"])
def get_bookmarks(username):
    if not username:
        return jsonify({"message": "Missing fields"}), 400
    
    try:
        recipes_query = text("""
                             SELECT r.recipe_id, r.author_username, r.publish_date, r.title, r.short_description, r.steps, r.time, r.servings, r.sustainability_rating, r.average_rating, i.ingredient_name, i.amount, i.weight
                             FROM recipe AS r
                             JOIN contains_ingredient as i
                             ON r.recipe_id = i.recipe_id
                             JOIN bookmark AS b ON r.recipe_id = b.recipe_id
                             WHERE b.username = :username
                             ORDER BY r.recipe_id DESC
                             """)
        
        result = db.session.execute(recipes_query, {"username": username}).fetchall()

        # convert Row objects to dictionaries
        rows = [row._mapping for row in result]

        recipes_dict = recipes_to_dict(rows)

        recipes_list = list(recipes_dict.values())
        return jsonify({"username": username, "bookmarks": recipes_list}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

#comment
@app.route("/comment", methods=["POST"])
def comment_recipe():
    data = request.get_json()
    recipe_id = data.get("recipe_id")
    username = data.get("username")
    content = data.get("content")

    if not (recipe_id and username and content):
        return jsonify({"message": "Missing comment info"}), 400

    try:
        sql = text("""
            INSERT INTO comment (recipe_id, username, publish_date, content)
            VALUES (:recipe_id, :username, NOW(), :content)
        """)
        db.session.execute(sql, {
            "recipe_id": recipe_id,
            "username": username,
            "content": content
        })
        db.session.commit()
        return jsonify({"message": "Comment added!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

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

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message" : "logged out"}), 200

# search (FULLTEXT index added to recipe(title, short_description, steps) columns a
@app.route("/search", methods=["GET"])
def search_recipes():
    search_term = request.json.get("search_term")

    if not search_term:
        return jsonify({"message": "Invalid data"}), 400
    
    try:
        sql = text("""
                    SELECT DISTINCT r.recipe_id, r.author_username, r.publish_date, r.title,
                                    r.short_description, r.steps, r.time, r.servings,
                                    r.sustainability_rating, r.average_rating,
                                    i.ingredient_name, i.amount, i.weight
                    FROM recipe AS r
                    JOIN contains_ingredient AS i ON r.recipe_id = i.recipe_id
                    WHERE MATCH(r.title, r.short_description, r.steps) AGAINST(:search_term in NATURAL LANGUAGE MODE)
                   """)
        result = db.session.execute(sql, {"search_term": search_term}).fetchall()
        # convert Row objects to dictionaries
        rows = [row._mapping for row in result]

        recipes_dict = recipes_to_dict(rows)

        recipes_list = list(recipes_dict.values())
        return jsonify({"search_results": recipes_list}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

def recipes_to_dict(rows):
    recipes_dict = {}
    for row in rows:
        recipe_id = row["recipe_id"]
        if recipe_id not in recipes_dict:
            # reformat time (total mins) to hrs and mins
            hours = row["time"] // 60
            mins = row["time"] % 60
            if hours > 0 and mins > 0:
                time = f"{hours} hr and {mins} min"
            elif hours > 0 and mins == 0:
                time = f"{hours} hr"
            else:
                time = f"{mins} min"
            
            average_rating = row["average_rating"] if row["average_rating"] is not None else "N/A"

            recipes_dict[recipe_id] = {
                "recipe_id": recipe_id,
                "author_username": row["author_username"].lower(),
                "publish_date": row["publish_date"],
                "title": row["title"],
                "short_description": row["short_description"],
                "steps": row["steps"],
                "time": time,
                "servings": row["servings"],
                "sustainability_rating": row["sustainability_rating"],
                "average_rating": average_rating,
                "ingredients": []
            }
        recipes_dict[recipe_id]["ingredients"].append({
            "ingredient_name": row["ingredient_name"],
            "amount": row["amount"],
            "weight": row["weight"]
        })

    return recipes_dict

    
# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)
