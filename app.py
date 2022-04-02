# pylint: disable= C0114, C0115, C0116, E1101
# The above is fine, but I'd prefer that the full names are used for less ambiguity (e.g. "missing-module-docstring")
# I'd also like for us to have justifications regarding the warnings we disable

from os import getenv

import flask
import requests


# Just for testing deployment; I used a separate file to fetch all env variables and imported them in other files for convenience
HOST = getenv("IP", "0.0.0.0")
PORT = int(getenv("PORT", "8080"))

app = flask.Flask(__name__)


@app.route("/")
def main():
    current_user = "Signed In User"
    return flask.render_template("index.html", current_user=current_user)


@app.route("/teams")
def teams():
    return flask.render_template("teams.html")


@app.route("/search_form", methods=["POST", "GET"])
def search():
    pokemon_name = flask.request.form.get("search")
    response = requests.get("https://pokeapi.co/api/v2/pokemon/" + pokemon_name + "/")
    data = response.json()
    headlines = {"name": "", "id": "", "image": "", "moves": []}
    headlines.update({"name": data["name"]})
    headlines.update({"id": data["id"]})
    headlines.update({"image": data["sprites"]["front_shiny"]})
    length_of_moves = len(data["moves"])
    list_of_moves = []
    for i in range(length_of_moves):
        list_of_moves.append(data["moves"][i]["move"]["name"])
    headlines.update({"moves": list_of_moves})
    print(list_of_moves)
    return flask.render_template(
        "search.html",
        headlines=headlines,
        pokemon_name=pokemon_name,
        length=length_of_moves,
    )


app.run(debug=True, host=HOST, port=PORT)
