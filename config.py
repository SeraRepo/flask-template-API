import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
SECRET_KEY = "myveryseeeecretkey"
URL_PREFIX = "/api/v1"
UPLOAD_FOLDER = os.path.join(basedir,'upload')