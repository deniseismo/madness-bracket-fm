import os
import sys
from flask import current_app


def load_unicode_extension(db_connection, _):
    """adds unicode extension to sqlite database for better searching

    Args:
        db_connection (db connection): [description]
    """
    file_extension = ".dll"
    if sys.platform == "linux":
        file_extension = ".so"
    filename = "unicode" + file_extension
    filepath = os.path.join(current_app.root_path, "db_extensions", filename)
    db_connection.enable_load_extension(True)
    db_connection.load_extension(filepath)
