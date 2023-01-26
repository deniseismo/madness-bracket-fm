import csv
import os

from flask import current_app

from madnessbracket import create_app, db
from madnessbracket.models import User

app = create_app()
app.app_context().push()

csv.field_size_limit(2147483647)


def add_new_users_from_csv() -> None:
    """
    adds new users from .csv file;
    can be used to manually transfer brackets saved as .csv
    """
    filename = "../user.csv"
    filepath = os.path.join(current_app.root_path, "dev/db_mgmt/user_mgmt", filename)

    newly_found_users_count = 0
    with open(filepath, encoding="utf-8") as file:
        csvfile = csv.DictReader(file)
        for line in csvfile:
            spotify_id = line["spotify_id"]
            spotify_token = line["spotify_token"]
            print(spotify_id, spotify_token)

            user_entry = User.query.filter(User.spotify_id == spotify_id).first()
            if user_entry:
                print(f"{user_entry} already exists, skipping...")
                continue
            new_user = User(spotify_id=spotify_id, spotify_token=spotify_token)
            print(f"adding new user: {new_user}")
            db.session.add(new_user)
            db.session.commit()
            newly_found_users_count += 1

    print(f"successfully added {newly_found_users_count} users.")


if __name__ == '__main__':
    add_new_users_from_csv()
