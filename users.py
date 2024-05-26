
# Library imports
from typing import Union, Tuple, List, Iterable, Dict
import json

# Project imports
from errors import NameAlreadyInUseError
from database import get_db, make_query
from util import escape, new_id, pickle_list, unpickle_list


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
            q = "SELECT * FROM users WHERE (name LIKE %s)"
            q = f"{q};" if limit < 0 else f"{q} LIMIT {limit};"
            cur.execute(make_query(q), [escape(name)])
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
    def register_game_ownership(cls, user_name_or_id: Union[str, int], game_id: int):
        """
        Adds the game id to the user's list of owned games. Duplicate entries are ignored
        :param user_name_or_id: (str or int) Pass the users exact name or user id
        :param game_id: (int) Specify the games id
        :return: None
        """
        user_id = user_name_or_id if isinstance(user_name_or_id, int) \
            else cls.search(user_name_or_id, exact_match=True)[0]["user_id"]

        games_list = cls.lookup(user_id)["games_owned"]
        games_list.append(game_id)

        with get_db() as db:
            cur = db.cursor()
            query = make_query(f"UPDATE users SET games_owned = '{pickle_list(set(games_list))}' WHERE user_id = %s;")
            cur.execute(query, [user_id])

        if user_id not in cls.own_this_game(game_id):
            print(cls.own_this_game(game_id))
            raise Exception(f"Update operation not successful, query: {query % user_id}")

    @classmethod
    def own_this_game(cls, game_id: int) -> List:
        """
        Fetch a list of user names that own a particular game
        :param game_id: (int) game id to check ownership of
        :return: List of user names
        """
        # Get a list of users (ignore users who don't own any games)
        with get_db() as db:
            cur = db.cursor()
            query = make_query(f"SELECT * FROM users WHERE games_owned IS NOT NULL;")
            cur.execute(query)
            user_list = [cls._user_dict(row) for row in cur.fetchall()]

        # Iterate through user list, and add to owners list if game id is in their owned games list
        owners_list = []
        game_id = int(game_id)
        for user in user_list:
            if game_id in user["games_owned"]:
                owners_list.append(user["name"])

        # Return the owners list
        owners_list.sort()
        return owners_list

    @classmethod
    def fetch_all_owned_games(cls) -> List:
        # Get a list of users (ignore users who don't own any games)
        with get_db() as db:
            cur = db.cursor()
            query = make_query(f"SELECT * FROM users WHERE games_owned IS NOT NULL;")
            cur.execute(query)
            user_list = [cls._user_dict(row) for row in cur.fetchall()]

        games_set = set()

        for user in user_list:
            for game in user["games_owned"]:
                games_set.add(int(game))

        return list(games_set)

    @classmethod
    def _user_dict(cls, value_list: Iterable) -> Dict:
        keys = ["user_id", "name", "games_owned", "data"]
        d = dict(zip(keys, value_list))
        d["games_owned"] = json.loads(d["games_owned"]) if d["games_owned"] else []
        d["data"] = json.loads(d["data"]) if d["data"] else []
        return d


if __name__ == "__main__":



    games = Users.fetch_all_owned_games()


    pass