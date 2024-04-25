

from database import get_db


class BGC:

    @classmethod
    def game_search(cls, name: str, exact_match=False):
        with get_db() as db:
            cur = db.cursor()
            name = name if exact_match else f"%{name}%"
            query = ("SELECT * FROM bgg_data WHERE (name LIKE %s);")
            cur.execute(query, [name])
            return cur.fetchall()

