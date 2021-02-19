import os
import json

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'etc'))
with open(os.path.join(file_path, 'config.json')) as config_file:
    config = json.load(config_file)


class Config:
    SECRET_KEY = config.get('SECRET_KEY')
    SERVER_NAME = config.get('SERVER_NAME')
    JSON_SORT_KEYS = False
    SQLALCHEMY_DATABASE_URI = config.get('SQLALCHEMY_DATABASE_URI')
    SPOTIFY_CLIENT_SECRET = config.get("SPOTIFY_CLIENT_SECRET")
    SPOTIFY_CLIENT_ID = config.get("SPOTIFY_CLIENT_ID")
    SPOTIFY_REDIRECT_URI = config.get("SPOTIFY_REDIRECT_URI")