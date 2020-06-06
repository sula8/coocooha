import os


class Config:
    DEBUG = True
    FLASK_DEBUG = 1
    SECRET_KEY = 'Developer'
    SECURITY_PASSWORD_SALT = 'sha512_crypt'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MEDIA_FOLDER = 'media'
