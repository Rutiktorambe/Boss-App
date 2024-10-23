import os

class Config:
    SECRET_KEY = 'winteriscoming'  # Updated secret key
    SQLALCHEMY_DATABASE_URI = 'sqlite:///ems_user.db'  # SQLite database in the same directory
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = 300  # 5 minutes session timeout
