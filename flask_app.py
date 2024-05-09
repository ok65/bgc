# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request, redirect, jsonify
from games import Games
from users import Users

app = Flask(__name__)


@app.route('/')
def default():
    return redirect("/home")

@app.route('/home', methods=["GET", "POST"])
def hello_world():
    query = request.values.get("query")
    print(query)
    #gl = GamesList.fetch_with_filter(query) if query else GamesList.fetch_all()
    return render_template("home.html", games_list=[])


@app.route("/search", methods=["GET", "POST"])
def search():
    search_str = request.values.get("search_query")
    results = Games.search(search_str) if search_str else []
    return render_template("search.html", search_list=results)


@app.route("/json/game_search", methods=["GET", "POST"])
def json_game_search():
    search_str = request.get_json()["search_query"]
    limit = request.get_json().get("limit", 10)
    results = Games.search(search_str, limit=limit) if search_str else []
    return jsonify(results)


@app.route("/json/user_search", methods=["GET", "POST"])
def json_user_search():
    search_str = request.get_json()["search_query"]
    limit = request.get_json().get("limit", 10)
    results = Users.search(search_str, limit=limit) if search_str else []
    return jsonify(results)


@app.route("/game/<game_id>", methods=["GET", "POST"])
def game(game_id):
    game_data = Games.lookup(game_id)
    return render_template("game.html", game_data=game_data)


@app.route("/users", methods=["GET", "POST"])
def users_all():
    user_id = request.values.get("user_id")
    if user_id:
        return render_template("users.html", user_list=None, user_data=Users.lookup(user_id))
    else:
        return render_template("users.html", user_list=Users.list(), user_data=None)


@app.route("/match")
def match():
    return render_template("match.html")



if __name__ == "__main__":

    app.run(debug=True)