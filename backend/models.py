from config import db
from datetime import datetime
from sqlalchemy import CheckConstraint

class Follow(db.Model):
    __tablename__ = "follow"
    username_follower = db.Column(db.String(256), db.ForeignKey("user.username", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    username_followee = db.Column(db.String(256), db.ForeignKey("user.username", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)

    __table_args__ = (
        db.PrimaryKeyConstraint("username_follower", "username_followee"),
    )

    def to_json(self):
        return {
            "usernameFollower": self.username_follower,
            "usernameFollowee": self.username_followee
        }


class Photo(db.Model):
    __tablename__ = "photo"
    photo_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    photo = db.Column(db.LargeBinary)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.recipe_id", onupdate="CASCADE", ondelete="CASCADE"))


class Rate(db.Model):
    __tablename__ = "rate"
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.recipe_id", onupdate="CASCADE", ondelete="CASCADE"))
    username = db.Column(db.String(256), db.ForeignKey("user.username", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    value = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.PrimaryKeyConstraint("recipe_id", "username"),
        CheckConstraint("value >= 1 AND value <= 10", name="rating_range"),
    )


class Likes(db.Model):
    __tablename__ = "likes"
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.recipe_id", onupdate="CASCADE", ondelete="CASCADE"))
    username = db.Column(db.String(256), db.ForeignKey("user.username", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    publish_date = db.Column(db.DateTime, default=datetime.now) # UTC timezone
    content = db.Column(db.String(256), nullable=False)

    __table_args__ = (
        db.PrimaryKeyConstraint("recipe_id", "username", "content"),
    )


class Comment(db.Model):
    __tablename__ = "comment"
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.recipe_id", onupdate="CASCADE", ondelete="CASCADE"))
    username = db.Column(db.String(256), db.ForeignKey("user.username", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)

    __table_args__ = (
        db.PrimaryKeyConstraint("recipe_id", "username"),
    )


class Bookmark(db.Model):
    __tablename__ = "bookmark"
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.recipe_id", onupdate="CASCADE", ondelete="CASCADE"))
    username = db.Column(db.String(256), db.ForeignKey("user.username", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)

    __table_args__ = (
        db.PrimaryKeyConstraint("recipe_id", "username"),
    )
    

class Recipe(db.Model):
    __tablename__ = "recipe"
    recipe_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_username = db.Column(db.String(256), db.ForeignKey("user.username", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    publish_date = db.Column(db.DateTime, default=datetime.now) # UTC timezone
    title = db.Column(db.String(60))
    short_description = db.Column(db.String(256))
    steps = db.Column(db.String(1000))
    time = db.Column(db.Integer, nullable=False)
    servings = db.Column(db.Integer, nullable=False)
    sustainability_rating = db.Column(db.Float)
    average_rating = db.Column(db.Float)

    # Recipe.photos gives you all Photo objects linked to this recipe / Photo.recipe (backref) gives the Recipe object linked to photo
    photos = db.relationship("Photo", foreign_keys=[Photo.recipe_id], backref="recipe", cascade="all, delete-orphan")
    # Recipe.rates gives you all Rate objects linked to this recipe / Rate.rated_recipe (backref) gives the Recipe object linked to the rate
    rates = db.relationship("Rate", foreign_keys=[Rate.recipe_id], backref="rated_recipe", cascade="all, delete-orphan")
    # Recipe.likes gives you all Likes objects linked to this recipe / Likes.liked_recipe (backref) gives the Recipe object linked to the rate
    likes = db.relationship("Likes", foreign_keys=[Likes.recipe_id], backref="liked_recipe", cascade="all, delete-orphan")
    # Recipe.comments gives you all Comment objects linked to this recipe / Comment.commented_recipe (backref) gives the Recipe object linked to the comment
    comments = db.relationship("Comment", foreign_keys=[Comment.recipe_id], backref="commented_recipe", cascade="all, delete-orphan")
    # Recipe.bookmarks gives you all Bookmark objects linked to this recipe / Bookmark.bookmarked_recipe (backref) gives the Recipe object linked to the bookmark
    bookmarks = db.relationship("Bookmark", foreign_keys=[Bookmark.recipe_id], backref="bookmarked_recipe", cascade="all, delete-orphan")

    def to_json(self):
        return {
            "recipeId": self.recipe_id,
            "authorUsername": self.author_username,
            "publish_date": self.publish_date,
            "title": self.title,
            "shortDescription": self.short_description,
            "steps": self.steps,
            "time": self.time,
            "servings": self.servings,
            "sustainabilityRating": self.sustainability_rating,
            "averageRating": self.average_rating
        }


class User(db.Model):
    __tablename__ = "user"
    username = db.Column(db.String(256), primary_key=True)
    password = db.Column(db.String(60), nullable=False)
    bio = db.Column(db.String(256))
    profile_picture = db.Column(db.LargeBinary)

    # User.followers gives all Follow objects where user is being followed / Follow.followee (backref) gives you corresponding User object who is being followed
    followers = db.relationship("Follow", foreign_keys=[Follow.username_followee], backref="followee", cascade="all, delete-orphan")
    # User.following gives all Follow objects where user is following others / Follow.follower (backref) gives you corresponding User object who is following others
    following = db.relationship("Follow", foreign_keys=[Follow.username_follower], backref="follower", cascade="all, delete-orphan")
    # User.recipes gives all Recipe objects the User created / Recipe.author (backref) gives the User object of the recipe
    recipes = db.relationship("Recipe", foreign_keys=[Recipe.author_username], backref="author", cascade="all, delete-orphan")
    # User.rates gives you all Rate objects the User has rated / Rate.rated_by (backref) gives the User object who gave the rating
    rates = db.relationship("Rate", foreign_keys=[Rate.username], backref="rated_by", cascade="all, delete-orphan")
    # User.likes gives you all Likes objects the User has liked / Likes.liked_by (backref) gives the User object who gave the like
    likes = db.relationship("Likes", foreign_keys=[Likes.username], backref="liked_by", cascade="all, delete-orphan")
    # User.comments gives you all the Comment objects the User has commented / Comment.commented_by (backref) gives the User object who gave the comment
    comments = db.relationship("Comment", foreign_keys=[Comment.username], backref="commented_by", cascade="all, delete-orphan")
    # User.bookmarks gives you all the Bookmark objects the User has bookmarked / Bookmark.bookmarked_by (backref) gives the User object who bookmarked
    bookmarks = db.relationship("Bookmark", foreign_keys=[Bookmark.username], backref="bookmarked_by", cascade="all, delete-orphan")

    def to_json(self):
        return {
            "username": self.username,
            "password": self.password,
            "bio": self.bio,
            "profilePicture": self.profile_picture
        }


# make these data models later
class Ingredient:
    pass

class Contains_Ingredient:
    pass