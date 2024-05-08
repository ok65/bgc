
# Library imports
from typing import Optional, Tuple, List, Iterable, Dict
import json

# Project imports
from errors import NameAlreadyInUseError
from database import get_db, make_query
from util import escape, new_id


class Users:

    @classmethod
    def search(cls, name: str, exact_match=False, limit: int = -1) -> List[Dict]:
        """
        Searches the user database for the name specified, and returns matching results
        :param name: (str) Name (or partial name) to search for
        :param exact_match: (bool) Do not match with partials
        :param limit: (int) max number of results to return (default of -1 means no limit)
        :return: List of dict of user data
        """
        with get_db() as db:
            cur = db.cursor()
            name = name if exact_match else f"%{name}%"
            query = make_query("SELECT * FROM users WHERE (name LIKE %s) LIMIT %s;")
            cur.execute(query, [escape(name), int(limit)])
            return [cls._user_dict(row) for row in cur.fetchall()]

    @classmethod
    def lookup(cls, user_id: int) -> Dict:
        """
        Lookup user by their user id, and return dict of data about them
        :param user_id: (int)
        :return: Dict of data about the game
        """
        with get_db() as db:
            cur = db.cursor()
            query = make_query("SELECT * FROM users WHERE (user_id = %s);")
            cur.execute(query, [int(user_id)])
            return cls._user_dict(cur.fetchone())

    @classmethod
    def add(cls, name) -> Tuple:
        """
        Add player to the database
        :param name: Player name string
        :return: Returns a tuple of the new user id and name
        """
        # Raise exception if name already in use
        if cls.search(name):
            raise NameAlreadyInUseError(repr(name))

        # Create new user id
        user_id = new_id()

        # Add name and ID to database
        with get_db() as db:
            cur = db.cursor()
            query = make_query("INSERT INTO users (user_id, name) VALUES (%s, %s);")
            cur.execute(query, (user_id, escape(name)))

        # Return name and user id tuple
        return (user_id, name)

    @classmethod
    def list(cls) -> List[Dict]:
        """
        Return a list of all users
        :return: List of users
        """

        with get_db() as db:
            cur = db.cursor()
            query = make_query("SELECT * FROM users;")
            cur.execute(query)
            return [cls._user_dict(row) for row in cur.fetchall()]

    @classmethod
    def _user_dict(cls, value_list: Iterable) -> Dict:
        keys = ["user_id", "name", "games_owned", "data"]
        d = dict(zip(keys, value_list))
        d["games_owned"] = json.loads(d["games_owned"]) if d["games_owned"] else []
        d["data"] = json.loads(d["data"]) if d["data"] else []
        return d

if __name__ == "__main__":

    r = Users.search("werter")


    pass