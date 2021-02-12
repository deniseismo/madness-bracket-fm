import json

with open("config.json") as config_file:
    config = json.load(config_file)


class Config:
    SECRET_KEY = config.get('SECRET_KEY')
    SERVER_NAME = '192.168.1.62:5000'
    JSON_SORT_KEYS = False
    SQLALCHEMY_DATABASE_URI = config.get('SQLALCHEMY_DATABASE_URI')