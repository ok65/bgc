
from boardgamegeek import BGGClient
import csv
import json
from database import get_db

bgg = BGGClient()

csv_file_path = "boardgames_ranks.csv"


with open(csv_file_path, "r") as fp:
    csv_reader = csv.reader(fp)

    header = next(csv_reader)



    for row in csv_reader:
        game_id = int(row[0])

        data = bgg.game(game_id=game_id).data()

        name = json.dumps(data.get("name"))
        image_url = json.dumps(data.get("image"))
        thumb_url = json.dumps(data.get("thumbnail"))
        categories = json.dumps(data.get("categories", []))
        designers = json.dumps(data.get("designers", []))
        artists = json.dumps(data.get("artists", []))
        players_min = int(data.get("minplayers", 0))
        players_max = int(data.get("maxplayers", 0))
        playtime_min = int(data.get("minplaytime", 0))
        playtime_max = int(data.get("maxplaytime", 0))
        mechanics = json.dumps(data.get("mechanics", []))
        family = json.dumps(data.get("families", []))

        query = ("INSERT INTO bgg_data "
                 "(game_id, name, image_url, thumb_url, categories, designers, artists, players_min, players_max, playtime_min, playtime_max, mechanics, family) "
                 f"VALUES ({game_id}, '{name}', '{image_url}', '{thumb_url}', '{categories}', '{designers}', '{artists}', {players_min}, {players_max}, {playtime_min}, {playtime_max}, '{mechanics}', '{family}')")

        print(query)

        try:
            with get_db() as db:
                cur = db.cursor()
                cur.execute(query)
                db.commit()
                cur.close()

        except:
            print(" !!!! SQL insert failed")
            print("  ")
            continue

        else:
            print("SQL insert passed")
            print("  ")


        pass


    print("##### ENTIRE DATASET COMPLETE #######")
    pass


