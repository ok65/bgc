
# Library imports
from typing import Optional, Dict, List, Iterable
from datetime import datetime
import json

# Project imports
from database import get_db, make_query, get_timeformat
from util import pickle_list, unpickle_list, pickle_dict, unpickle_dict


class Match:

    @classmethod
    def register(cls, game_id: int, players: List, scores: List, score_type: str, meta_data: Optional[Dict] = None):

        # Prepare data
        meta_data = meta_data if meta_data else {}
        meta_data["score_type"] = score_type
        stamp = datetime.now().strftime(get_timeformat())

        # Prepare query
        query = make_query("INSERT INTO match_results (game_id, players, data, scores, datetime) "
                           "VALUES (%s, %s, %s, %s, %s);")

        # Open db, and execute insertion query
        with get_db() as db:
            cur = db.cursor()
            cur.execute(query, [game_id, pickle_list(players), pickle_dict(meta_data), pickle_list(scores), stamp])
            cur.close()

    @classmethod
    def fetch_by_game(cls, game_id: int) -> List:
        # Prepare select query
        query = make_query("SELECT * FROM match_results WHERE game_id = %s ORDER BY datetime DESC")

        # Open db and perform query
        with get_db() as db:
            cur = db.cursor()
            cur.execute(query, [int(game_id)])
            return [cls._match_dict(x) for x in cur.fetchall()]

    @classmethod
    def fetch_by_player(cls, player: str) -> List:
        # Prepare select query
        query = make_query("SELECT * FROM match_results WHERE players LIKE %s")

        # Open db and perform query
        with get_db() as db:
            cur = db.cursor()
            cur.execute(query, [f"%{player}%"])
            return [cls._match_dict(x) for x in cur.fetchall()]

    @classmethod
    def _match_dict(cls, value_list: Iterable):
        keys = ["match_id", "game_id", "players", "data", "scores", "datetime"]
        md = dict(zip(keys, value_list))

        md["players"] = unpickle_list(md["players"])
        md["data"] = unpickle_dict(md["data"])
        md["scores"] = [int(x) for x in unpickle_list(md["scores"])] if md["scores"] else None
        if not isinstance(md["datetime"], datetime):
            md["datetime"] = datetime.strptime(md["datetime"], get_timeformat())
        return md






if __name__ == "__main__":

    Match.register(game_id=188, player_score_dict={"Sammy": 75, "John": 42, "Tim": 123}, meta_data={"hitler": "Dick"})

    matches = Match.fetch_by_game(188)

    peter_matches = Match.fetch_by_player("peter")

    pass