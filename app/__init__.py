import os
from flask import Flask
from flask_login import LoginManager
# from flask_wtf.csrf import CSRFProtect
from app.extensions import mongo
from app.blueprints.auth import auth_bp 
from app.blueprints.products import products_bp 
from app.blueprints.auth.models import User
 # Assuming you have auth blueprint in 'auth' module
# Import your User model here if needed

login_manager = LoginManager()
UPLOAD_FOLDER = 'app/static/uploads'

# Ensure that the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object('config.Config')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # Initialize extensions
    mongo.init_app(app)
    login_manager.init_app(app)  # Initialize the LoginManager with the app

    # Set the login view (this is the view the user is redirected to if not logged in)
    login_manager.login_view = 'auth.login'

    # Register the user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return User.get_user_by_id(user_id)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(products_bp, url_prefix='/product')

    return app
