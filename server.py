from flask import Flask, request
import queries
import insert_data_to_tables


app = Flask(__name__, static_url_path='', static_folder='rings')


@app.route('/pokemon_by_trainer/<trainer_name>', methods=["GET"])
def get_pokemon_by_trainer(trainer_name):
    try:
        return str(queries.find_roster(trainer_name)), 200
    except Exception as e:
        return "couldn't get pokemon by that trainer: " + str(e), 400


@app.route('/trainers_by_pokemon/<pokemon_name>', methods=["GET"])
def get_trainers_by_pokemon(pokemon_name):
    try:
        return str(queries.find_owners(pokemon_name)), 200
    except Exception as e:
        return "couldn't get trainers by that pokemon: " + str(e), 400


@app.route('/add_pokemon', methods=["POST"])
def add_pokemon():
    pokemon = request.get_json()
    try:
        insert_data_to_tables.insert_to_tables2(pokemon)
        return "the pokemon added successfully", 201
    except Exception as e:
        return "couldn't add that pokemon: " + str(e), 400


@app.route('/get_pokemon_by_type/<type_>', methods=["GET"])
def get_pokemon_by_type(type_):
    try:
        return ", ".join(queries.find_by_type(type_)), 200
    except Exception as e:
        return "couldn't get pokemon by that type: " + str(e), 400


@app.route('/get_heaviest_pokemon', methods=["GET"])
def get_heaviest_pokemon():

    try:
        return str(queries.find_heaviest_pokemon()), 200
    except Exception as e:
        return "couldn't get the trainer with the most pokemon: " + str(e), 400


@app.route('/get_trainer_with_most_pokemon', methods=["GET"])
def get_trainer_with_most_pokemon():

    try:
        return ", ".join(queries.find_trainer_with_most_pokemon()), 200
    except Exception as e:
        return "couldn't get the heaviest pokemon: " + str(e), 400


@app.route('/get_ring/<pokemon_id>', methods=["GET"])
def get_ring(pokemon_id):

    try:
        return app.send_static_file(f'Ring0{queries.find_type(pokemon_id) % 10}.wav'), 200
    except Exception as e:
        return "couldn't get the ring of that type: " + str(e), 400


if __name__ == '__main__':
    app.run(port=3000)
