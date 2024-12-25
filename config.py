import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'e_commerce')
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/e_commerce_db')
    DEBUG = True