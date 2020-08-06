import pymysql


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

            return int(res_list[0]["type_id"])
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
            return result
    except:
        raise ValueError("couldn't find the heaviest pokemon")


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


def find_trainer_with_most_pokemon():
    try:
        with connection.cursor() as cursor:
            query0 = "CREATE TEMPORARY TABLE temp_table select t.count, t.trainer_id from (select trainer_id,count(pokemon_id) as count from ownedby group by trainer_id) as t"
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
