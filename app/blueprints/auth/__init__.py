from flask import Blueprint

# Initialize the auth blueprint
auth_bp = Blueprint('auth', __name__, template_folder='templates', static_folder='static')

# Import routes to register them with the blueprint
from . import routes