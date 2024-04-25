

from database import get_db


class BGC:

    @classmethod
    def game_search(cls, name: str, exact_match=False):
        with get_db() as db:
            cur = db.cursor()
            if exact_match:
                query = ("SELECT * FROM bgg_data WHERE (name = %s);")
            else:
                query = ("SELECT * FROM bgg_data WHERE (name LIKE %%s%);")
            cur.execute(query, name)
            return cur.fetchall()

