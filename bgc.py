
from uuid import uuid4
from database import get_db
from util import escape
from typing import List, Tuple


class NameAlreadyInUseError(Exception): pass


class BGC:

    @classmethod
    def game_search(cls, name: str, exact_match=False) -> List:
        with get_db() as db:
            cur = db.cursor()
            name = name if exact_match else f"%{name}%"
            query = ("SELECT * FROM bgg_data WHERE (name LIKE %s);")
            cur.execute(query, [escape(name)])
            return cur.fetchall()

    @classmethod
    def user_search(cls, name: str, exact_match=True) -> List:
        with get_db() as db:
            cur = db.cursor()
            name = name if exact_match else f"%{name}%"
            query = ("SELECT * FROM users WHERE (name LIKE %s);")
            cur.execute(query, [escape(name)])
            return cur.fetchall()

    @classmethod
    def add_player(cls, name) -> Tuple:
        # Raise exception if name already in use
        if cls.user_search(name):
            raise NameAlreadyInUseError(repr(name))

        # Create new user id
        user_id = cls._new_id()

        # Add user name and ID to database
        with get_db() as db:
            cur = db.cursor()
            query = ("INSERT INTO users (user_id, name) VALUES (%s, '%s');")
            cur.execute(query, [user_id, escape(name)])

        # Return name and user id tuple
        return (user_id, name)




    @classmethod
    def _new_id(cls) -> int:
        return uuid4().int & 0xFFFF


