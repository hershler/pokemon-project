from flask import Flask, request, render_template
import queries
import insert_data_to_tables


app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')


@app.route("/")
def root():
    return render_template('index.html')


@app.route('/select_pokemon')
def select_pokemon():
    return render_template("select_pokemon.html")


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


@app.route('/update_pokemon_types/<pokemon_name>', methods=["PUT"])
def update_pokemon_types(pokemon_name):
    try:
        return str(queries.update_types(pokemon_name)), 200
    except Exception as e:
        return "couldn't update types of that pokemon: " + str(e), 400


@app.route("/delete_trainer's_pokemon/", methods=["DELETE"])
def delete_pokemon():
    req = request.get_json()
    pokemon = req["pokemon"]
    trainer = req["trainer"]

    try:
        queries.delete_owned_by(pokemon, trainer)
        return "deleting done successfully", 204
    except Exception as e:
        return "couldn't delete that pokemon of that trainer: " + str(e), 400


@app.route('/pokemon_by_type/<type_>', methods=["GET"])
def get_pokemon_by_type(type_):
    try:
        return ", ".join(queries.find_by_type(type_)), 200
    except Exception as e:
        return "couldn't get pokemon by that type: " + str(e), 400


@app.route('/trainer_with_most_pokemon', methods=["GET"])
def get_heaviest_pokemon():

    try:
        return str(queries.find_heaviest_pokemon()), 200
    except Exception as e:
        return "couldn't get the trainer with the most pokemon: " + str(e), 400


@app.route('/heaviest_pokemon', methods=["GET"])
def get_trainer_with_most_pokemon():

    try:
        return ", ".join(queries.find_trainer_with_most_pokemon()), 200
    except Exception as e:
        return "couldn't get the heaviest pokemon: " + str(e), 400


@app.route('/get_ring', methods=["GET"])
def get_ring():

    pokemon_id = request.args.get("pokemon_id")

    print(pokemon_id)
    try:
        lst_type = queries.find_type(pokemon_id)
        num_ring = lst_type[0] % 10
        return app.send_static_file(f'rings/Ring0{num_ring}.wav'), 200
    except Exception as e:
        return "couldn't get the ring of that type: " + str(e), 400


if __name__ == '__main__':
    app.run(port=3000)
