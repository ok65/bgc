
from boardgamegeek import BGGClient, BGGApiRetryError
import csv
import json
from database import get_db
import time

bgg = BGGClient(requests_per_minute=400)

csv_file_path = "boardgames_ranks.csv"


def escape(raw_string) -> str:
    raw_string = "" if raw_string is None else raw_string
    return raw_string.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\t', '\\t').replace('\r', '\\r').replace("'", "\\'")


session_count = 0

if __name__ == "__main__":

    while True:
        with open(csv_file_path, "r") as fp:
            csv_reader = csv.reader(fp)

            header = next(csv_reader)
            for row in csv_reader:
                game_id = int(row[0])

                with get_db() as db:
                    cur = db.cursor()
                    cur.execute(f"SELECT (game_id) FROM bgg_data WHERE (game_id={game_id})")
                    result = cur.fetchall()
                    db.commit()
                    cur.close()

                if result:
                    print(f"skipping {game_id}, already in sql db")
                    break

                data = None

                for x in range(3):

                    try:
                        print(f"BGG look attempt {x}")
                        data = bgg.game(game_id=game_id).data()

                    except Exception as error:
                        time.sleep(1)

                    else:
                        break

                if not isinstance(data, dict):
                    print(f"bad data, skipping game {game_id}")
                    continue

                name = escape(data.get("name", ""))
                print(type(data.get("image", "")))
                image_url = escape(data.get("image", ""))
                thumb_url = escape(data.get("thumbnail", ""))
                categories = ", ".join([escape(x) for x in data.get("categories", [])])
                designers = ", ".join([escape(x) for x in data.get("designers", [])])
                artists = ", ".join([escape(x) for x in data.get("artists", [])])
                players_min = int(data.get("minplayers", 0))
                players_max = int(data.get("maxplayers", 0))
                playtime_min = int(data.get("minplaytime", 0))
                playtime_max = int(data.get("maxplaytime", 0))
                mechanics = ", ".join([escape(x) for x in data.get("mechanics", [])])
                family = ", ".join([escape(x) for x in data.get("families", [])])
                year_published = data.get("yearpublished ", 0)
                description = escape(data.get("description", ""))

                query = ("INSERT INTO bgg_data "
                         "(game_id, name, image_url, thumb_url, categories, designers, artists, players_min, players_max, playtime_min, playtime_max, mechanics, family, year_published, description) "
                         f"VALUES ({game_id}, '{name}', '{image_url}', '{thumb_url}', '[{categories}]', '[{designers}]', '[{artists}]', {players_min}, {players_max}, {playtime_min}, {playtime_max}, '[{mechanics}]', '[{family}]', {year_published}, '{description}')")

                print(query)

                session_count += 1

                print(session_count)


                try:
                    with get_db() as db:
                        cur = db.cursor()
                        cur.execute(query)
                        db.commit()
                        cur.close()

                except Exception as error:
                    print(" !!!! SQL insert failed")
                    print(error)
                    print("  ")
                    continue

                else:
                    print("SQL insert passed")
                    print("  ")


                pass


            print("##### ENTIRE DATASET COMPLETE #######")
            pass


