import pymysql
import requests


connection = pymysql.connect(
    host="localhost",
    user="root",
    password="1",
    db="sql_pokemon",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)


def find_roster(owner_name):
    try:
        with connection.cursor() as cursor:
            query = "select t_id from trainer where t_name = '{}'".format(owner_name)
            cursor.execute(query)
            owner_id = cursor.fetchall()

            query = "select pokemon_id from ownedBy where trainer_id = '{}'".format(owner_id[0]['t_id'])
            cursor.execute(query)
            pokemon_id = cursor.fetchall()

            pokemon_list = set()

            for pokemon in pokemon_id:
                query = "select p_name from pokemon where p_id = {}".format(pokemon['pokemon_id'])
                cursor.execute(query)
                pokemon_name = cursor.fetchall()
                pokemon_list.add(pokemon_name[0]['p_name'])

        return pokemon_list
    except:
        raise ValueError("couldn't find pokemon by that roster")


def find_owners(pokemon_name):
    try:
        with connection.cursor() as cursor:
            query = "select p_id from pokemon where p_name = '{}'".format(pokemon_name)
            cursor.execute(query)
            pokemon_id = cursor.fetchall()

            query = "select trainer_id from ownedby where pokemon_id = '{}'".format(pokemon_id[0]['p_id'])
            cursor.execute(query)
            owner_id = cursor.fetchall()

            owner_list = set()

            for owner in owner_id:
                query = "select t_name from trainer where t_id = {}".format(owner['trainer_id'])
                cursor.execute(query)
                owner_name = cursor.fetchall()
                owner_list.add(owner_name[0]['t_name'])

        return owner_list
    except:
        raise ValueError("couldn't find owner")


def find_type(pokemon_id):
    try:
        with connection.cursor() as cursor:
            query = "select type_id from typeOf where pokemon_id = {}".format(pokemon_id)
            cursor.execute(query)
            res_list = cursor.fetchall()

            return [item["type_id"] for item in res_list]
    except:
        raise ValueError("couldn't find the type")


def find_heaviest_pokemon():
    try:
        with connection.cursor() as cursor:
            query = "SELECT MAX(p_weight) FROM pokemon"
            cursor.execute(query)
            result = cursor.fetchall()
            query = "SELECT p_name FROM pokemon WHERE p_weight = {}".format(result[0]['MAX(p_weight)'])
            cursor.execute(query)
            result = cursor.fetchall()
            return result[0]["p_name"]
    except:
        raise ValueError("couldn't find the heaviest pokemon")


def find_p_id_by_name(name):
    try:
        with connection.cursor() as cursor:
            query = "SELECT p_id FROM pokemon WHERE p_name = {} ".format(name)
            cursor.execute(query)
            return cursor.fetchall()[0]["p_id"]
    except:
        raise ValueError("couldn't find id of that name")


def find_t_id_by_name(name):
    try:
        with connection.cursor() as cursor:
            query = "SELECT t_id FROM trainer WHERE t_name = {} ".format(name)
            cursor.execute(query)
            return cursor.fetchall()[0]["t_id"]
    except:
        raise ValueError("couldn't find id of that name")


def find_by_type(type_):
    try:
        with connection.cursor() as cursor:
            query = "select pt_id from pokemonType where pt_name = '{}'".format(type_)
            cursor.execute(query)
            type_id = cursor.fetchall()
            query = """select p_name from pokemon 
            where p_id in (select pokemon_id from typeOf where type_id = {})""".format(type_id[0]['pt_id'])
            cursor.execute(query)
            result = cursor.fetchall()
            return [res['p_name'] for res in result]
    except:
        raise ValueError("couldn't find pokemon by that type")


def delete_owned_by(trainer, pokemon):
    try:
        with connection.cursor() as cursor:
            pokemon_id = find_p_id_by_name(pokemon)
            trainer_id = find_t_id_by_name(trainer)

            query = "DELETE FROM ownedBy WHERE pokemon_id = {} and trainer = {}".format(pokemon_id, trainer_id)
            cursor.execute(query)
    except:
        raise ValueError("couldn't delete that ownedBy")


def find_trainer_with_most_pokemon():
    try:
        with connection.cursor() as cursor:
            query0 = "CREATE TEMPORARY TABLE temp_table select t.count, t.trainer_id from (select trainer_id, count(pokemon_id) as count from ownedby group by trainer_id) as t"
            cursor.execute(query0)

            query1 = "select MAX(count) as max from temp_table"
            cursor.execute(query1)
            count = cursor.fetchall()

            query2 = "select trainer_id from temp_table where count = {}".format(count[0]['max'])
            cursor.execute(query2)
            owner_id = cursor.fetchall()

            owner_max_pokemon = list()

            for owner in owner_id:
                query3 = "select t_name from trainer where t_id = {}".format(owner['trainer_id'])
                cursor.execute(query3)
                owner_name = cursor.fetchall()
                owner_max_pokemon.append(owner_name[0]['t_name'])
            return owner_max_pokemon

    except:
        raise ValueError("couldn't find the trainer with the most pokemon")


def update_types(pokemon_name):
    try:
        pokemon_url = "https://pokeapi.co/api/v2/pokemon/{}".format(pokemon_name)
        poke_api_types = (requests.get(url=pokemon_url, verify=False).json())["types"]
        with connection.cursor() as cursor:
            query = "select p_id from pokemon where p_name = '{}'".format(pokemon_name)
            cursor.execute(query)
            pokemon_id = cursor.fetchall()[0]["p_id"]
            updated_types = find_type(pokemon_id)
            for type_ in poke_api_types:
                query = "select pt_id from pokemonType where pt_name = '{}'".format(type_["type"]["name"])
                cursor.execute(query)
                pokemon_type_id = cursor.fetchall()[0]["pt_id"]
                if pokemon_type_id not in updated_types:
                    query = "INSERT INTO typeOf(type_id, pokemon_id) values('{}', '{}')".format(pokemon_type_id, pokemon_id)
                    cursor.execute(query)
                    connection.commit()
            return "the pokemon's types updated successfully"
    except:
        raise ValueError("couldn't update the pokemon's type")
