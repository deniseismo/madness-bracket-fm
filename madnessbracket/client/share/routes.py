import json
import urllib.parse

from flask import render_template, Blueprint, jsonify, request, make_response, Response

from madnessbracket.client.database_manipulation.db_bracket_handlers import save_bracket_to_database, \
    get_bracket_from_database
from madnessbracket.client.share.share_handlers import parse_bracket_data_for_sharing
from madnessbracket.utilities.validation.bracket_data_validation import validate_bracket_data
from madnessbracket.utilities.validation.exceptions.validation_exceptions import BracketDataError
from madnessbracket.utilities.validation.user_input_validation import is_valid_nanoid

share = Blueprint('share', __name__)


@share.route('/share', methods=['POST'])
def share_madness_bracket() -> Response:
    """
    share madness bracket: save madness bracket data to db → get share link for the bracket
    :return: jsonified dict with the share link for the madness bracket
    """
    bracket_share_data = request.get_json()
    # validate bracket data via pydantic models
    try:
        validated_bracket_data = validate_bracket_data(bracket_share_data)
    except BracketDataError as e:
        return make_response(jsonify(
            {'message': str(e)}
        ),
            404)
    # parse pydantic models to get an appropriate dict structure for sharing
    parsed_bracket_data = parse_bracket_data_for_sharing(validated_bracket_data)
    # get bracket unique id used for sharing
    bracket_share_link_id = save_bracket_to_database(parsed_bracket_data)
    return jsonify({
        "bracketShareLink": urllib.parse.urljoin("get/", bracket_share_link_id)
    })


@share.route("/get/<bracket_id>", methods=["GET"])
def get_shared_bracket(bracket_id: str):
    """
    get shared bracket (saved in database) by bracket share link id
    :param bracket_id: (str): (uuid4-like string) bracket share link id
    """
    if not is_valid_nanoid(bracket_id):
        print("invalid bracket id")
        return render_template("404.html")
    shared_bracket_data = get_bracket_from_database(
        bracket_id)
    if not shared_bracket_data:
        error_message = "bracket not found"
        return render_template("404.html", error_message=error_message)
    shared_bracket_data = json.dumps(shared_bracket_data)

    return render_template("shared.html", shared_bracket_data=shared_bracket_data)
