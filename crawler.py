
from boardgamegeek import BGGClient
import csv
from database import get_db

bgg = BGGClient()

csv_file_path = "boardgames_ranks.csv"


with open(csv_file_path, "r") as fp:
    csv_reader = csv.reader(fp)

    header = next(csv_reader)

    json = {}

    for row in csv_reader:
        game_id = int(row[0])

        data = bgg.game(game_id=game_id).data()

        name = data.get("name")
        image_url = data.get("image")
        thumb_url = data.get("thumbnail")
        categories = ", ".join(data.get("categories", []))
        designers = ", ".join(data.get("designers", []))
        artists = ", ".join(data.get("artists", []))
        players_min = int(data.get("min_players", 0))
        players_max = int(data.get("max_players", 0))
        playtime_min = int(data.get("min_playtime", 0))
        playtime_max = int(data.get("max_playtime", 0))
        mechanics = ", ".join(data.get("mechanics", []))
        family = ", ".join(data.get("family", []))

        query = ("INSERT INTO bgg_data "
                 "(game_id, name, image_url, thumb_url, categories, designers, artists, players_min, players_max, playtime_min, playtime_max, mechanics, family) "
                 f"VALUES ({game_id}, '{name}', '{image_url}', '{thumb_url}', '{categories}', '{designers}', '{artists}', {players_min}, {players_max}, {playtime_min}, {playtime_max}, '{mechanics}', '{family}')")

        print(query)

        with get_db() as db:
            cur = db.cursor()
            cur.execute(query)
            db.commit()
            cur.close()

        pass


    print("##### ENTIRE DATASET COMPLETE #######")
    pass