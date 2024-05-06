
# Library imports
from uuid import uuid4
from typing import Iterable, List


def escape(raw_string: str) -> str:
    raw_string = "" if raw_string is None else str(raw_string)
    return raw_string.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\t', '\\t').replace('\r', '\\r').replace("'", "\\'")


def pickle_list(in_list: Iterable) -> str:
    return "["+", ".join([escape(x) for x in in_list])+"]"


def unpickle_list(picked_list: str) -> List:
    return picked_list[1:-1].split(", ")


def new_id() -> int:
    return uuid4().int & 0xFFFF

