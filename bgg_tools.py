
from boardgamegeek import BGGClient
from typing import Dict


def bgg_lookup(name: str) -> Dict:
    bgg = BGGClient()
    return bgg.game(name).data()


if __name__ == "__main__":

    data = bgg_lookup("Monopoly")
    pass