
from boardgamegeek import BGGClient
from typing import Dict, List

_client = BGGClient(requests_per_minute=100)


def bgg_id_lookup(game_id: int) -> Dict:
    bgg = _client
    return bgg.game(game_id=game_id).data()


def bgg_search(name: str, sort_most_likely: bool = True) -> List[Dict]:
    bgg = _client
    r = [x.data() for x in bgg.search(name)]
    return sorted(r, key=lambda x: x["yearpublished"], reverse=True)


if __name__ == "__main__":

    import time

    #data = bgg_lookup("Monopoly")

    start = time.time()
    results = bgg_search("Heat")

    gl = []
    for game in results[:10]:
        gl.append(bgg_id_lookup(game["id"]))

    duration = time.time() - start
    print(f"took {duration} seconds")

    pass