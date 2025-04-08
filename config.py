import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-should-change-this'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///todo.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
