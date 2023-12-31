import os


class Config:
    DEBUG = True
    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:pgsql@localhost:5432/fyyur"

APP_HOST = "0.0.0.0"
APP_PORT = 3000

