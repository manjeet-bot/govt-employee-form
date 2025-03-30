import os

class Config:
    SECRET_KEY = 'supersecretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'  # Later PostgreSQL ke liye change karenge
    SQLALCHEMY_TRACK_MODIFICATIONS = False
