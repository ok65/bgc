# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request, redirect
#from games_list import GamesList
from bgg_tools import *
from bgc import BGC

app = Flask(__name__)


@app.route('/')
def default():
    return redirect("/home.html")

@app.route('/home.html', methods=["GET", "POST"])
def hello_world():
    query = request.values.get("query")
    print(query)
    #gl = GamesList.fetch_with_filter(query) if query else GamesList.fetch_all()
    return render_template("home.html", games_list=[])


@app.route("/search.html", methods=["GET", "POST"])
def search():
    search_str = request.values.get("search_query")
    results = BGC.game_search(search_str) if search_str else []
    return render_template("search.html", search_list=results)


if __name__ == "__main__":

    app.run(debug=True)