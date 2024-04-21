
import json
import time

from filelock import Timeout, FileLock
from typing import List, Dict, Optional
#from bgg_tools import bgg_lookup

_JSON_FILE = "games_list.json"
_LOCK_FILE = "games_list.json.LOCK"


class GameIdAlreadyExistsError(Exception): pass
class GameIdNotPresentError(Exception): pass


class GamesList:

    def __init__(self):
        pass

    @classmethod
    def fetch_all(cls) -> List:
        with open(_JSON_FILE, "r") as fp:
            return json.load(fp)

    @classmethod
    def fetch_with_filter(cls, _filter:str) -> List:
        return cls._apply_filter(cls.fetch_all(), _filter)

    @classmethod
    def fetch_by_owner(cls, owner: str) -> List:
        gl = cls.fetch_all()
        return [g for g in gl if owner in g.get("owners", [])]

    @classmethod
    def fetch_by_id(cls, bgg_id: int) -> Optional[Dict]:
        gl = cls.fetch_all()
        results = [g for g in gl if g.get("bgg_id") == bgg_id]
        return results[0] if results else None

    """
    @classmethod
    def add_game(cls, name: str, owners: List):

        bgg_data = bgg_lookup(name)
        if cls.fetch_by_id(bgg_data["id"]):
            raise GameIdAlreadyExistsError

        game = {"bgg_id": bgg_data["id"],
                "name": bgg_data["name"],
                "image_url": bgg_data.get("image", None),
                "thumbnail_url": bgg_data.get("thumbnail", None),
                "categories": bgg_data.get("categories", []),
                "designers": bgg_data.get("designers", []),
                "artists": bgg_data.get("artists", []),
                "players_min": bgg_data.get("minplayers", 0),
                "players_max": bgg_data.get("maxplayers", 0),
                "playtime_min": bgg_data.get("minplaytime", 0),
                "playtime_max": bgg_data.get("maxplaytime", 0),
                "bgg_rating": bgg_data["stats"]["average"],
                "bgg_ranking": bgg_data["stats"]["ranks"][0]["value"],
                "owners": owners,
                "bgc_rating": -1,
                "bgc_stats": [],
                "year": bgg_data["yearpublished"]
                }

        lock = FileLock(_LOCK_FILE)
        with lock.acquire(timeout=1):
            gl = cls.fetch_all()
            gl.append(game)
            with open(_JSON_FILE, "w") as fp:
                json.dump(gl, fp)
    """
    @classmethod
    def add_owners(cls, bgg_id: int, owners: List):

        if not cls.fetch_by_id(bgg_id):
            raise GameIdNotPresentError

        lock = FileLock(_LOCK_FILE)
        with lock.acquire(timeout=1):
            gl = cls.fetch_all()
            game = [g for g in gl if g["bgg_id"] == bgg_id][0]
            game["owners"].extend(owners)
            with open(_JSON_FILE, "w") as fp:
                json.dump(gl, fp)

    @classmethod
    def add_bgc_score(cls, bgg_id: int, score: float):
        if score < 1 or score < 0:
            raise Exception("Score must be between 0 and 1")

        lock = FileLock(_LOCK_FILE)
        with lock.acquire(timeout=1):
            gl = cls.fetch_all()
            game = [g for g in gl if g["bgg_id"] == bgg_id][0]
            #game["bgc_stats"].append("score": score, "timestamp": time.time())
            with open(_JSON_FILE, "w") as fp:
                json.dump(gl, fp)

    @classmethod
    def _apply_filter(cls, data, filter_string):
        filtered_data = data[:]
        filters = filter_string.strip().split()

        for filter_item in filters:
            attribute, operator, value = None, None, None

            for sep in ['>', '<', '~', ':']:
                if sep in filter_item:
                    attribute, operator, value = filter_item.partition(sep)
                    operator = operator.strip()
                    value = value.strip()
                    break

            if operator == '>':
                filtered_data = [item for item in filtered_data if item.get(attribute, 0) > float(value)]
            elif operator == '<':
                filtered_data = [item for item in filtered_data if item.get(attribute, 0) < float(value)]
            elif operator == '~':
                filtered_data = [item for item in filtered_data if value.lower() in item.get(attribute, '').lower()]
            elif operator == ':':
                if value.isnumeric():
                    filtered_data = [item for item in filtered_data if str(value) == str(item.get(attribute))]
                else:
                    filtered_data = [item for item in filtered_data if str(value) in str(item.get(attribute))]

        return filtered_data



if __name__ == "__main__":

    big_list = ["Wavelength",
    "Mysterium",
    "Monikers",
    "7 wonders",
    "Magic maze",
    "6 Nimmt",
    "Sushi go party",
    "Game of thrones",
    "Citadels",
    "Zoo Vadis",
    "Scythe",
    "Perudo / Liars dice",
    "King of tokyo",
    "Lords of waterdeep",
    "Coup",
    "Love letter",
    "Ra",
    "Modern Art",
    "Pictomania",
    "Carcassone",
    "Dixit",
    "Men at work",
    "colt express",
    "Heat! Pedal to the metal",
    "Istanbul",
    "The crew",
    "Exploding kittens",
    "Bohnanza",
    "Cosmic encounter",
    "Ethnos",
    "Monopoly Deal",
    "Chronicles of crime",
    "Kemet",
    "colt express",
    "Dune",
    "Pandemic",
    "Splendor",
    "Survive, escape from atlantis",
    "Unlock 10",
    "Inis",
    "Root",
    "Cubitos",
    "Imperial settlers",
    "Galaxy trucker",
    "Cascadia",
    "Great western trail",
    "This war of mine",
    "M11 at rush hour",
    "Spirit Island",
    "Arboretum",
    "The",
    "Quacks of Quedlinburg",
    "Azul"]

    for game in big_list:

        try:
            GamesList.add_game(game, [])
        except:
            print(f"Failed trying to add {game}")
            continue
        else:
            print(f"Added {game} to db")

    print("done")

    pass

