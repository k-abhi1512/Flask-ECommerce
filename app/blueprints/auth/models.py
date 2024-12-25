from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import mongo
from bson.objectid import ObjectId

class User(UserMixin):
    def __init__(self, username, email, password, _id=None):
        self.username = username
        self.email = email
        self.password = password
        self._id = _id  # Store the MongoDB _id

    def save_to_db(self):
        hashed_password = generate_password_hash(self.password)
        user = {
            'username': self.username,
            'email': self.email,
            'password': hashed_password
        }
        result = mongo.db.users.insert_one(user)
        self._id = result.inserted_id  # Update the user with the MongoDB _id
        return self

    @staticmethod
    def find_by_email(email):
        user_data = mongo.db.users.find_one({'email': email})
        if user_data:
            return User(**user_data)  # Return a User instance
        return None
    
    @staticmethod
    def verify_password(stored_password, provided_password):
        return check_password_hash(stored_password, provided_password)

    @staticmethod
    def get_user_by_id(user_id):
        try:
            user_data = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        except Exception as e:
            print(f"Error while converting user_id to ObjectId: {e}")
            return None
        if user_data:
            return User(**user_data)  # Return a User instance
        return None
    
    def get_id(self):
        # Use the MongoDB _id as the identifier for Flask-Login
        return str(self._id)  # Return the ObjectId as a string

    # Optional: Define any custom methods like is_active, etc.
    def is_active(self):
        return True  # You can add your own logic here if needed
