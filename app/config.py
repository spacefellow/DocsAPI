from os import path, getenv


class Config(object):
    basedir = path.abspath(path.dirname(__file__))
    ELASTICSEARCH_URL = getenv('ELASTICSEARCH_URL')
    SECRET_KEY = getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URL", "postgresql://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True


app_config = Config()
