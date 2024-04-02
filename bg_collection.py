
from database import get_db
from boardgamegeek import BGGClient
import json


class BGCollection:

    def __init__(self):
        pass

    def add(self, name: str, owner: str, dummy=True):
        bgg = BGGClient()
        game = bgg.game(name)
        query = ("INSERT INTO games VALUES "
                 "(game_id, name, players_min, players_max, description)"
                 "VALUES (%s, %s, %s, %s, %s)")
        with get_db() as db:
            cur = db.cursor()
            cur.execute(query, (game.id, game.name, game.min_players, game.max_players, game.description))
            cur.commit()
            cur.close()
            print(f"New game added, id: {game.id}")

