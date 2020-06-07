import os


class DevConfig:
    FLASK_ENV='development'
    SECRET_KEY = 'Developer'
    SECURITY_PASSWORD_SALT = 'sha512_crypt'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
    SQLALCHEMY_DATABASE_URI = (os.environ.get("DATABASE_URL") or \
                               'postgresql+psycopg2://postgres:postgres@127.0.0.1:5432/coocooha')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MEDIA_FOLDER = 'media'
