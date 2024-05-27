# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request, redirect, jsonify
from games import Games
from users import Users
from match import Match

app = Flask(__name__)


@app.route('/')
def default():
    return redirect("/home")


@app.route('/home', methods=["GET", "POST"])
def hello_world():
    query = request.values.get("query")
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


@app.route("/json/ownership_register", methods=["GET", "POST"])
def json_ownership_register():
    owner_name = request.get_json()["owner_name"]
    game_id = request.get_json()["game_id"]
    Users.register_game_ownership(owner_name, game_id=game_id)
    return jsonify({"operation": "success"})


@app.route("/json/match_register", methods=["GET", "POST"])
def json_match_register():
    game_id = request.get_json()["game_id"]
    players = request.get_json()["players"]
    scores = request.get_json()["scores"]
    score_type = request.get_json()["score_type"]
    bad_player = request.get_json()["bad"]
    meta_data = {"bad": bad_player} if bad_player else {}
    Match.register(game_id=game_id, players=players, scores=scores, score_type=score_type, meta_data=meta_data)
    return jsonify({"operation": "success"})


@app.route("/game/<game_id>", methods=["GET", "POST"])
def game(game_id):
    game_data = Games.lookup(game_id)
    owner_list = Users.own_this_game(game_id)
    recent_plays = Match.fetch_by_game(game_id)[:10]
    return render_template("game.html", game_data=game_data, owner_list=owner_list, recent_plays=recent_plays)


@app.route("/users", methods=["GET", "POST"])
def users_all():
    user_id = request.values.get("user_id")
    if user_id:
        return render_template("users.html", user_list=None, user_data=Users.lookup(user_id))
    else:
        return render_template("users.html", user_list=Users.list(), user_data=None)


@app.route("/listing")
def listing():
    game_id_list = Users.fetch_all_owned_games()
    game_list = Games.list_lookup(game_id_list)
    return render_template("listing.html", game_list=game_list)


@app.route("/match")
def match():
    return render_template("match.html")



if __name__ == "__main__":

    app.run(debug=True)