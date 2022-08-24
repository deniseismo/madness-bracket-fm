from flask import render_template, Blueprint

from madnessbracket.client.profile.spotify.spotify_profile_oauth import check_spotify_login, get_spotify_user_info

main = Blueprint('main', __name__)


@main.route("/", methods=["GET", "POST"])
@main.route("/home", methods=["GET", "POST"])
def home() -> str:
    """renders home page

    Returns:
        home page template (home.html)
    """
    user, token = check_spotify_login()
    spotify_info = {
        "logged_in": user and token,
        "user_info": get_spotify_user_info(token.access_token) if (user and token) else None
    }
    return render_template("home.html", spotify_info=spotify_info)


@main.route("/about", methods=["GET"])
def about() -> str:
    """renders about page

    Returns:
        about page template (home.html)
    """
    return render_template("about.html", title="About")
