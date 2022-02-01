import json
import urllib.parse

from flask import render_template, Blueprint, jsonify, request, make_response, Response

from madnessbracket.share.bracket_data_validation import (validate_bracket_data_for_sharing,
                                                          parse_bracket_data_for_sharing, is_valid_nanoid)
from madnessbracket.share.share_handlers import save_bracket_to_database, get_bracket_from_database

share = Blueprint('share', __name__)


@share.route('/share', methods=['POST'])
def get_share_link() -> Response:
    """save bracket to the database → get share link to the bracket
    """
    content = request.get_json()
    print(content)
    print(content["description"])
    # validate bracket data via pydantic models
    validated_bracket_data = validate_bracket_data_for_sharing(content)
    if not validated_bracket_data:
        return make_response("Invalid Bracket Data", 400)
    # parse pydantic models to get an appropriate dict structure for sharing
    parsed_bracket_data = parse_bracket_data_for_sharing(
        validated_bracket_data)
    # get bracket unique id used for sharing
    share_link_id = save_bracket_to_database(parsed_bracket_data)
    return jsonify({
        "bracketShareLink": urllib.parse.urljoin("get/", share_link_id)
    })


@share.route("/get/<bracket_id>", methods=["GET"])
def get_shared_bracket(bracket_id) -> str:
    """get/generate a bracket from a given bracket id that is presumably stored in a database

    Args:
        bracket_id (str): uuid4-like string

    Returns:
        html: template
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
