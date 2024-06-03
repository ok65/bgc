
# Library imports
from typing import Optional, Dict, List, Iterable, Tuple
from datetime import datetime
import json

# Project imports
from database import get_db, make_query, get_timeformat
from util import pickle_list, unpickle_list, pickle_dict, unpickle_dict


class Match:

    @classmethod
    def register(cls, game_id: int, player_id_list: List[int], scores: List, meta_data: Optional[Dict] = None):

        # Prepare data
        meta_data = meta_data if meta_data else {}
        stamp = datetime.now().strftime(get_timeformat())

        # Prepare query
        query = make_query("INSERT INTO match_results (game_id, players, data, scores, datetime) "
                           "VALUES (%s, %s, %s, %s, %s);")

        # Open db, and execute insertion query
        with get_db() as db:
            cur = db.cursor()
            cur.execute(query, [game_id, pickle_list(player_id_list), pickle_dict(meta_data), pickle_list(scores), stamp])
            cur.close()

    @classmethod
    def fetch_by_game(cls, game_id: int, limit=-1) -> List:
        # Prepare select query
        q = "SELECT * FROM match_results WHERE game_id = %s ORDER BY datetime DESC"
        q = f"{q};" if limit < 0 else f"{q} LIMIT {limit};"

        # Open db and perform query
        with get_db() as db:
            cur = db.cursor()
            cur.execute(make_query(q), [int(game_id)])
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
    def fetch_top_players_by_game(cls, game_id: int) -> Tuple[List, List]:
        player_scores = {}
        for match in cls.fetch_by_game(game_id):
            for player, score in zip(match["players"], match["scores"]):
                player_scores[player] = max(score, player_scores[player]) if player in player_scores else score

        top_scores = sorted(player_scores.items(), key=lambda x: x[1], reverse=True)

        return [x[0] for x in top_scores[:10]], [x[1] for x in top_scores[:10]]

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



    pass