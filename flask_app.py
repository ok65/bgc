# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template
from games_list import GamesList

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("home.html", games_list=GamesList.fetch_all())


if __name__ == "__main__":

    app.run()