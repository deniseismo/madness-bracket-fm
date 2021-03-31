import os
import csv
from flask import current_app


def log_missing_info(info):
    """
    logs missing info (missing songs/albums/releases, etc.) to a file
    """
    filename = 'missing_info.csv'
    filepath = os.path.join(current_app.root_path, 'dev/logs', filename)
    try:
        with open(filepath, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([info])
    except IOError as e:
        print('file not found', e)
        return None
