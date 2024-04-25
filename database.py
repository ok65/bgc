
import mysql.connector
import json

with open("secrets.json", "r") as fp:
    MYSQL_PW = json.load(fp)["MYSQLPW"]
MYSQL_DB = "ok65$bgc"



def get_db():
    return mysql.connector.connect(host="ok65.mysql.pythonanywhere-services.com", user="ok65", password=MYSQL_PW, database=MYSQL_DB)
