

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

    # Loop the crawler forever
    while True:

        try:
            # Open the bgg ranked game csv file (ro)
            with open(csv_file_path, "r") as fp:

                # Parse csv
                csv_reader = csv.reader(fp)

                # Grab the first line as the column titles
                header = next(csv_reader)

                # Iterate through each row of the csv file
                for row in csv_reader:

                    # Pull game id from the first col
                    game_id = int(row[0])

                    # Open sql db connection, check if game id is already present
                    with get_db() as db:
                        cur = db.cursor()
                        cur.execute(f"SELECT (game_id) FROM bgg_data WHERE (game_id={game_id})")
                        result = cur.fetchall()
                        db.commit()
                        cur.close()

                    # If game id already present, skip this csv entry and move to the next
                    if result:
                        print(f"skipping {game_id}, already in sql db")
                        continue

                    # Make sure data initialises to none
                    data = None

                    # Try and pull BGG data from API 3 times
                    for x in range(3):
                        try:
                            print(f"BGG look attempt {x}")
                            data = bgg.game(game_id=game_id).data()

                        # On any errors (nasty code) sleep for 2 seconds, then iterate round and try again
                        except Exception as error:
                            time.sleep(2)

                        # BGG api call successful, break the for loop
                        else:
                            break

                    # After the 3 attempts if the data isn't a valid dict, skip this csv row and go to the next.
                    if not isinstance(data, dict):
                        print(f"bad data, skipping game {game_id}")
                        continue

                    # Extract all the useful info fromt he BGG api data
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
                    year_published = data.get("yearpublished", 0)
                    description = escape(data.get("description", ""))

                    # Prepare sql insertion query to store the game data
                    query = ("INSERT INTO bgg_data "
                             "(game_id, name, image_url, thumb_url, categories, designers, artists, players_min, players_max, playtime_min, playtime_max, mechanics, family, year_published, description) "
                             f"VALUES ({game_id}, '{name}', '{image_url}', '{thumb_url}', '[{categories}]', '[{designers}]', '[{artists}]', {players_min}, {players_max}, {playtime_min}, {playtime_max}, '[{mechanics}]', '[{family}]', {year_published}, '{description}')")

                    # Print the query and the number of insertions this session
                    print(query)
                    session_count += 1
                    print(session_count)

                    # Execute the sql query
                    try:
                        with get_db() as db:
                            cur = db.cursor()
                            cur.execute(query)
                            db.commit()
                            cur.close()

                    # If there is any error, print failure and skip to next csv row
                    except Exception as error:
                        print(" !!!! SQL insert failed")
                        print(error)
                        print("  ")
                        continue

                    # Insertion successful, print success and move to next csv row
                    else:
                        print("SQL insert passed")
                        print("  ")

                # If we get here we got to the end of the csv file.
                # Loop back to the top and start again.
                print("##### ENTIRE DATASET COMPLETE #######")
                pass

        except:
            continue


