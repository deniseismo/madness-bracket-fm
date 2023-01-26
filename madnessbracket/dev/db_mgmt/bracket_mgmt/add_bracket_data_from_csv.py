import csv
import os

from flask import current_app

from madnessbracket import create_app, db
from madnessbracket.models import BracketData

app = create_app()
app.app_context().push()

csv.field_size_limit(2147483647)


def add_bracket_data_from_csv_to_database() -> None:
    """
    adds bracket data given all the info in .csv file;
    can be used to manually transfer brackets saved as .csv
    """
    filename = "bracket_data.csv"
    filepath = os.path.join(current_app.root_path, "dev/db_mgmt/bracket_mgmt", filename)
    with open(filepath, encoding="utf-8") as file:
        csvfile = csv.DictReader(file)
        for line in csvfile:
            bracket_id = line["bracket_id"]
            title = line["title"]
            bracket_info = line["bracket_info"]
            winner = line["winner"]
            bracket_type = line["bracket_type"]
            print(title, winner)

            bracket = BracketData(bracket_id=bracket_id, title=title,
                                  bracket_info=bracket_info, winner=winner,
                                  bracket_type=bracket_type, value1=title)
            db.session.add(bracket)
            db.session.commit()


if __name__ == '__main__':
    add_bracket_data_from_csv_to_database()
