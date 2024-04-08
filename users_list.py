
import json
from filelock import Timeout, FileLock
from typing import List, Dict, Optional
from bgg_tools import bgg_lookup
from uuid import uuid4

_JSON_FILE = "users_list.json"
_LOCK_FILE = "users_list.json.LOCK"


class UsersList:

    def __init__(self):
        pass

    @classmethod
    def fetch_all(cls) -> List:
        with open(_JSON_FILE, "r") as fp:
            return json.load(fp)

    @classmethod
    def fetch_by_name(cls, name: str):
        ul = cls.fetch_all()
        result = [u for u in ul if u["name"] == name]
        return result[0] if result else None

    @classmethod
    def fetch_by_id(cls, _id: int):
        ul = cls.fetch_all()
        result = [u for u in ul if u["id"] == _id]
        return result[0] if result else None

    @classmethod
    def add_user(cls, name: str):

        if cls.fetch_by_name(name):
            raise Exception("User already exists")

        user = {"name": name,
                "id": cls._new_id()}

        lock = FileLock(_LOCK_FILE)
        with lock.acquire(timeout=1):
            ul = cls.fetch_all()
            ul.append(user)
            with open(_JSON_FILE, "w") as fp:
                json.dump(ul, fp)

    @classmethod
    def change_user_name(cls, _id: int, new_name: str):
        if not cls.fetch_by_id(_id):
            raise Exception("User already exists")

        lock = FileLock(_LOCK_FILE)
        with lock.acquire(timeout=1):
            ul = cls.fetch_all()
            user = [u for u in ul if u["id"] == _id][0]
            user["name"] = new_name
            with open(_JSON_FILE, "w") as fp:
                json.dump(ul, fp)

    @classmethod
    def _new_id(cls) -> int:
        return uuid4().int & 0xFFFF


if __name__ == "__main__":

    UsersList.add_user("Percy")
    pass