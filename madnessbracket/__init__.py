from flask import Flask
from flask_caching import Cache
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

from madnessbracket.config import Config, CACHE_CONFIG

my_naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
mtd = MetaData(naming_convention=my_naming_convention)
db = SQLAlchemy(metadata=mtd)

sess = Session()
cache = Cache()


def create_app(production=False, config_class=Config):
    """
    creates an instance of an app
    :param config_class: a config (Config class/object)
    :param production: whether the app's in testing or production mode. default: False
    :return: app
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    sess.init_app(app)
    if production:
        cache.init_app(app, config=CACHE_CONFIG["production"])
    else:
        cache.init_app(app, config=CACHE_CONFIG["testing"])
    db.init_app(app)
    # import all blueprints necessary
    from madnessbracket.client.main.routes import main
    from madnessbracket.client.profile.spotify.routes import spotify
    from madnessbracket.client.share.routes import share
    from madnessbracket.client.charts.routes import charts
    from madnessbracket.client.artist.routes import artist
    from madnessbracket.client.secret.routes import secret
    from madnessbracket.client.battle.routes import battle
    from madnessbracket.client.errors.handlers import errors
    from madnessbracket.client.trivia.routes import trivia
    from madnessbracket.client.profile.lastfm.routes import lastfm_profile

    # register all blueprints
    app.register_blueprint(main)
    app.register_blueprint(artist)
    app.register_blueprint(charts)
    app.register_blueprint(secret)
    app.register_blueprint(spotify)
    app.register_blueprint(share)
    app.register_blueprint(errors)
    app.register_blueprint(trivia)
    app.register_blueprint(lastfm_profile)
    app.register_blueprint(battle)

    return app
