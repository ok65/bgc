
from database import get_db
from boardgamegeek import BGGClient
import json


class BGCollection:

    def __init__(self):
        pass

    def add(self, name: str, owner: str, dummy=True):
        bgg = BGGClient()
        game = bgg.game(name)
        bgg_json = json.dumps(game.data())
        query = ("INSERT INTO bg_coll VALUES "
                 "(id, bgg_data, club_data, dummy)"
                 "VALUES (%s, %s, %s, %s)")
        with get_db() as db:
            cur = db.cursor()
            cur.execute(query, (game.id, bgg_json, "{}", 1))
            cur.commit()
            cur.close()
            print(f"New game added, id: {game.id}")

