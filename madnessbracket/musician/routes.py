import json

from flask import Blueprint, jsonify, request, make_response, render_template

from madnessbracket.musician.musician_handlers import get_artists_tracks
from madnessbracket.utilities.user_input_validation import validate_artist_name, validate_bracket_upper_limit

musician = Blueprint('musician', __name__)


@musician.route('/artist', methods=['POST', "GET"])
def generate_musician_bracket():
    """generates madness bracket for a particular artist/musician
    Returns:
        jsonified dict with all the tracks and tracks' info needed for the bracket
    """
    if request.method == "GET":
        artist_name = request.args.get("name")
        upper_limit = request.args.get("limit")
        valid_artist_name = validate_artist_name(artist_name)
        valid_upper_limit = validate_bracket_upper_limit(upper_limit)
        if not valid_artist_name or not valid_upper_limit:
            return render_template('404.html', title='Incorrect Input'), 404

        user_request = json.dumps({
            "bracket_type": "artist",
            "name": artist_name,
            "limit": upper_limit
        })
        return render_template("bracket.html", user_request=user_request)
    else:
        artist_name = request.args.get("name")
        upper_limit = request.args.get("limit")
        valid_artist_name = validate_artist_name(artist_name)
        valid_upper_limit = validate_bracket_upper_limit(upper_limit)
        if not valid_artist_name or not valid_upper_limit:
            print('no input')
            return make_response(jsonify(
                {'message': f"something's gone wrong"}
            ),
                404)
        upper_limit = valid_upper_limit.upper_limit
        tracks = get_artists_tracks(artist_name, upper_limit)
        print(tracks)
        if not tracks:
            print('nothing found')
            return make_response(jsonify(
                {'message': f"no tracks found for {artist_name}"}
            ),
                404)
        return jsonify(tracks)
