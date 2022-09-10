from flask import render_template, Blueprint

from madnessbracket.music_apis.spotify_api.spotify_user_handlers import authenticate_spotify_user, get_spotify_user_info

main = Blueprint('main', __name__)


@main.route("/", methods=["GET", "POST"])
@main.route("/home", methods=["GET", "POST"])
def home() -> str:
    """render home page"""
    user, token = authenticate_spotify_user()
    spotify_info = {
        "logged_in": user and token,
        "user_info": get_spotify_user_info(token.access_token) if (user and token) else None
    }
    return render_template("home.html", spotify_info=spotify_info)


@main.route("/about", methods=["GET"])
def about() -> str:
    """render about page"""
    return render_template("about.html", title="About")
