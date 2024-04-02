
import os
import mysql.connector

MYSQL_PW = os.environ["MYSQLPW"]
MYSQL_DB = "ok65$bgc"


def get_db():
    return mysql.connector.connect(host="ok65.mysql.pythonanywhere-services.com", user="ok65", password=MYSQL_PW, database=MYSQL_DB)