
# Library imports
import mysql.connector
import json
import sqlite3
from mysql.connector.abstracts import MySQLConnectionAbstract
from typing import Tuple

with open("secrets.json", "r") as fp:
    data = json.load(fp)
    MYSQL_PW = data.get("MYSQLPW", "null")
    SERVER_DEPLOYED = data.get("SERVER_DEPLOYED", False)

MYSQL_DB = "ok65$bgc"


def get_db() -> MySQLConnectionAbstract | sqlite3.Connection:
    """
    Convience function to connect to the database and return a connection object. Returns mysql connection when deployed
    to the server, and a local sqlite3 connection when not.
    :return: mysql/sqlite3 Connection Object
    """
    if SERVER_DEPLOYED:
        return mysql.connector.connect(host="ok65.mysql.pythonanywhere-services.com", user="ok65", password=MYSQL_PW, database=MYSQL_DB)
    else:
        return sqlite3.connect("dummy_sql.db")


def make_query(query) -> str:
    """
    sqlite3 prefers ? to %s for query variables, this function just switches between them automatically for you.
    :param query string with %s for variable replacement
    :return: string
    """
    if SERVER_DEPLOYED:
        return query
    else:
        return query.replace("%s", "?")
