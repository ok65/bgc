# Library imports
from typing import List, Dict, Iterable

# Project imports
from database import get_db, make_query
from util import escape


class Games:

    @classmethod
    def search(cls, name: str, exact_match=False, sort_similarity: bool = True, limit: int = -1) -> List[Dict]:
        """
        Search for a game by its title, and return a list of possible matches as dicts of data,
        :param limit: (int) Max number of results to return, default of -1 means no limit
        :param sort_similarity: (bool) Default true, will return more matches with better similarity score
        :param name: (str) Name to match to, partial or full
        :param exact_match: bool, if false it will find partial matches - if true an exact match only
        :return: List of dicts
        """
        from difflib import SequenceMatcher

        def similarity(a):
            return SequenceMatcher(None, name, a).ratio()

        with get_db() as db:
            cur = db.cursor()
            name = name if exact_match else f"%{name}%"
            q = "SELECT * FROM bgg_data WHERE (name LIKE %s) ORDER BY year_published DESC"
            query = make_query(f"{q} LIMIT {int(limit)};")
            cur.execute(query, [escape(name)])
            games = [cls._game_dict(row) for row in cur.fetchall()]
            games.sort(key=lambda x: similarity(x["name"]), reverse=True)
            return games

    @classmethod
    def lookup(cls, game_id: int) -> Dict:
        """
        Lookup game by its BGG game id, and return dict of data about it
        :param game_id: (int) game id
        :return: Dict of data about the game
        """
        with get_db() as db:
            cur = db.cursor()
            query = make_query("SELECT * FROM bgg_data WHERE (game_id = %s);")
            cur.execute(query, [int(game_id)])
            return cls._game_dict(cur.fetchone())

    @classmethod
    def _game_dict(cls, value_list: Iterable) -> Dict:
        keys = ["game_id", "name", "image_url", "thumb_url", "categories", "designers",
                "artists", "players_min", "players_max", "playtime_min", "playtime_max",
                "mechanics", "family", "year_published", "description"]
        gd = dict(zip(keys, value_list))

        gd["categories"] = gd["categories"][1:-1].split(", ")
        gd["designers"] = gd["designers"][1:-1].split(", ")
        gd["artists"] = gd["artists"][1:-1].split(", ")
        gd["mechanics"] = gd["mechanics"][1:-1].split(", ")
        gd["family"] = gd["family"][1:-1].split(", ")

        return gd


if __name__ == "__main__":
    r = Games.search("Monopoly", limit=10)

    r = Games.lookup(164840)

    pass
