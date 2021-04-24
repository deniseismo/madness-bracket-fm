import json
import os

file_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'etc'))
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
    LASTFM_API_KEY = config.get("LASTFM_API_KEY")
    LASTFM_USER_AGENT = config.get("LASTFM_USER_AGENT")
    MUSIC_BRAINZ_USER_AGENT = config.get("MUSIC_BRAINZ_USER_AGENT")
    DISCOGS_USER_TOKEN = config.get("DISCOGS_USER_TOKEN")
    APP_NAME = config.get("APP_NAME")


CACHE_CONFIG = {
    "production": {'CACHE_TYPE': 'redis', 'CACHE_KEY_PREFIX': 'fcache',
                   'CACHE_REDIS_HOST': 'localhost',
                   'CACHE_REDIS_PORT': '6379',
                   'CACHE_REDIS_URL': 'redis://localhost:6379'
                   },
    "testing": {'CACHE_TYPE': 'simple'}
}
