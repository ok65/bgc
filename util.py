
# Library imports
from uuid import uuid4
from typing import Iterable, List, Dict
from datetime import datetime, timedelta, timezone
import pytz


def escape(raw_string: str) -> str:
    raw_string = "" if raw_string is None else str(raw_string)
    return raw_string.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\t', '\\t').replace('\r', '\\r').replace("'", "\\'")


def pickle_list(in_list: Iterable) -> str:
    return "["+", ".join([escape(x) for x in in_list])+"]"


def unpickle_list(picked_list: str) -> List:
    return picked_list[1:-1].split(", ")


def pickle_dict(in_dict: Dict) -> str:
    flat = [item for pair in in_dict.items() for item in pair]
    return "{" + ", ".join([escape(x) for x in flat]) + "}"


def unpickle_dict(pickled_dict: str) -> Dict:
    flat = pickled_dict[1:-1].split(", ")
    return {flat[i]: flat[i + 1] for i in range(0, len(flat), 2)}


def new_id() -> int:
    return uuid4().int & 0xFFFF


def time_ago_in_words(dt):
    uk_timezone = pytz.timezone('Europe/London')
    now = datetime.now(uk_timezone)
    dt_uk = dt.astimezone(uk_timezone)  # Convert dt to UK timezone
    diff = now - dt_uk

    if diff < timedelta(minutes=10):
        return "just now"
    elif diff < timedelta(days=7):
        minutes = diff.seconds // 60
        if minutes < 60:
            return f"{minutes} minutes ago"
        else:
            hours = minutes // 60
            if hours == 1:
                return "1 hour ago"
            else:
                return f"{hours} hours ago"
    else:
        return dt.strftime("%Y-%m-%d")


if __name__ == "__main__":

    dt = datetime(2024, 5, 26, 23, 0, tzinfo=pytz.timezone("Europe/London"))
    print(time_ago_in_words(dt))