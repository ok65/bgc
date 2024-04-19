
from boardgamegeek import BGGClient
from typing import Dict


def bgg_lookup(name: str) -> Dict:
    bgg = BGGClient()
    return [x.data() for x in bgg.search(name, exact=True)]


if __name__ == "__main__":

    data = bgg_lookup("Monopoly")




    pass