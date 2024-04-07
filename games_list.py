
import json
from filelock import Timeout, FileLock
from typing import List, Dict, Optional
from bgg_tools import bgg_lookup

_JSON_FILE = "games_list.json"
_LOCK_FILE = "games_list.json.LOCK"


class GamesList:

    def __init__(self):
        pass

    @classmethod
    def fetch_all(cls) -> List:
        with open(_JSON_FILE, "r") as fp:
            return json.load(fp)

    @classmethod
    def fetch_by_owner(cls, owner: str) -> List:
        gl = cls.fetch_all()
        return [g for g in gl if owner in g.get("owners", [])]

    @classmethod
    def fetch_by_id(cls, bgg_id: int) -> Optional[Dict]:
        gl = cls.fetch_all()
        results = [g for g in gl if g.get("bgg_id") == bgg_id]
        return results[0] if results else None

    @classmethod
    def add_game(cls, name: str, owners: List):

        bgg_data = bgg_lookup(name)
        if cls.fetch_by_id(bgg_data["id"]):
            raise Exception("Game ID already in database")

        game = {"bgg_id": bgg_data["id"],
                "name": bgg_data["name"],
                "image_url": bgg_data.get("image", None),
                "thumbnail": bgg_data.get("thumbnail", None),
                "categories": bgg_data.get("categories", []),
                "designers": bgg_data.get("designers", []),
                "artists": bgg_data.get("artists", []),
                "players_min": bgg_data.get("minplayers", 0),
                "players_max": bgg_data.get("maxplayers", 0),
                "playtime_min": bgg_data.get("minplaytime", 0),
                "playtime_max": bgg_data.get("maxplaytime", 0),
                "bgg_rating": bgg_data["stats"]["average"],
                "owners": owners
                }

        lock = FileLock(_LOCK_FILE)
        with lock.acquire(timeout=1):
            gl = cls.fetch_all()
            gl.append(game)
            with open(_JSON_FILE, "w") as fp:
                json.dump(gl, fp)

    @classmethod
    def add_owners(cls, bgg_id: int, owners: List):

        if not cls.fetch_by_id(bgg_id):
            raise Exception("Game ID not in database")

        lock = FileLock(_LOCK_FILE)
        with lock.acquire(timeout=1):
            gl = cls.fetch_all()
            game = [g for g in gl if g["bgg_id"] == bgg_id][0]
            game["owners"].extend(owners)
            with open(_JSON_FILE, "w") as fp:
                json.dump(gl, fp)


if __name__ == "__main__":



    GamesList.add_owners(118, ["Tom", "Dick", "Harry"])

    pass