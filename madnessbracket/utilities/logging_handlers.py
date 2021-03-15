import csv


def log_missing_info(info):
    """
    logs missing info (missing songs/albums/releases, etc.) to a file
    """
    with open('madnessbracket/dev/logs/missing_info.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([info])