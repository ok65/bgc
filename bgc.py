
# Library imports
from uuid import uuid4
from typing import List, Tuple, Dict

# Project imports
from database import get_db
from util import escape


class BGC:

    @classmethod
    def _new_id(cls) -> int:
        return uuid4().int & 0xFFFF


