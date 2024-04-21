
from boardgamegeek import BGGClient
import csv
from database import get_db

bgg = BGGClient()

csv_file_path = "boardgames_ranks.csv"

db = get_db()

with open(csv_file_path, "r") as fp:
    csv_reader = csv.reader(fp)

    header = next(csv_reader)

    json = {}

    for row in csv_reader:
        d = {key: value for key, value in zip(header, row)}

        query = ("INSERT INTO bgg_data "
                 "(game_id, name, image_url, thumb_url, categories, designers, artists, players_min, players_max, playtime_min, playtime_max, mechanics, family) "
                 "VALUES ()")
        pass





    pass