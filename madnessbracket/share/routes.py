import uuid
import json
from flask import render_template, Blueprint, jsonify, request
from madnessbracket.share.share_handlers import save_bracket_to_database, get_bracket_from_database
from madnessbracket.share.data_validation import validate_bracket_data_for_sharing, parse_bracket_data_for_sharing, is_valid_uuid
share = Blueprint('share', __name__)


@share.route('/share', methods=['POST'])
def get_share_link():
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
        "success": share_link_id
    })


@share.route("/get/<bracket_id>", methods=["GET", "POST"])
def get_shared_bracket(bracket_id):
    """get/generate a bracket from a given bracket id that is presumably stored in a database

    Args:
        bracket_id (str): uuid4-like string

    Returns:
        html: template
    """
    print(is_valid_uuid(bracket_id))

    if request.method == "GET":
        data = get_bracket_from_database(bracket_id)
        if not data:
            return render_template("404.html")
        print("data:", data)
        return render_template("bracket.html", data=data)
    else:
        data = get_bracket_from_database(bracket_id)
        return jsonify(data)
