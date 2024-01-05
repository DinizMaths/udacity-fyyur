import os


class Config:
    DEBUG = True
    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:pgsql@localhost:5432/fyyur"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

APP_HOST = "0.0.0.0"
APP_PORT = 3000
