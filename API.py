from flask import Flask, Response, request
import json
import queries
import insert_data_to_tables


app = Flask(__name__)


@app.route('/pokemon_by_trainer/<trainer_name>', methods=["GET"])
def get_pokemon_by_trainer(trainer_name):
    return str(queries.findRoster(trainer_name))


@app.route('/trainers_by_pokemo/<pokemon_name>', methods=["GET"])
def get_trainers_by_pokemon(pokemon_name):
    return str(queries.findOwners(pokemon_name))


@app.route('/add_pokemon', methods=["POST"])
def add_pokemon():
    pokemon = request.get_json()
    try:
        insert_data_to_tables.insert_to_tables2(pokemon)
        return "the pokemon added successfuly"
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(port=3000)