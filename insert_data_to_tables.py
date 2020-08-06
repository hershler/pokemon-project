import json
import pymysql


connection = pymysql.connect(
    host="localhost",
    user="root",
    password="1",
    db="sql_pokemon",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)


def insert_to_pokemon_type(type):
    with connection.cursor() as cursor:
        query = "SELECT pt_id FROM pokemonType where pt_name = '{}'".format(type)
        cursor.execute(query)
        result = cursor.fetchall()
        
        if result:
            return result[0]['pt_id']

        try:
            with connection.cursor() as cursor:
                query = 'INSERT into pokemonType (pt_name) values ("{}")'.format(type)
                cursor.execute(query)
                connection.commit()
        except:
            print("Error in insert_to_pokemonType")
        
        with connection.cursor() as cursor:
            query = "SELECT pt_id FROM pokemonType where pt_name = '{}'".format(type)
            cursor.execute(query)
            result = cursor.fetchall()
            return result[0]['pt_id']
            

def insert_to_pokemon(id, name, height, weight):
    try:
        with connection.cursor() as cursor:
            query = 'INSERT into pokemon (p_id, p_name, p_height, p_weight) values ({}, "{}", {}, {})'.format(id, name, height, weight)
            cursor.execute(query)
            connection.commit()
    except:
        print("Error in insert_to_pokemon")


def insert_to_trainer(owner):
    id_owner_list = list()

    for owner_ in owner:
        with connection.cursor() as cursor:
            query = "SELECT t_id FROM trainer where t_name = '{}' and t_town = '{}'".format(owner_['name'], owner_['town'])
            cursor.execute(query)
            result = cursor.fetchall()
            
            if result:
                id_owner_list.append(result[0]['t_id'])
            
            else:
                try:
                    with connection.cursor() as cursor:
                        query = "INSERT into trainer (t_name, t_town) values ('{}', '{}')".format(owner_["name"], owner_["town"])
                        cursor.execute(query)
                        connection.commit()
                except:
                    print("Error in insert_to_trainer")
                
                with connection.cursor() as cursor:
                    query = "SELECT t_id FROM trainer where t_name = '{}' and t_town = '{}'".format(owner_["name"], owner_["town"])
                    cursor.execute(query)
                    result = cursor.fetchall()
                    id_owner_list.append(result[0]['t_id'])   
    
    return id_owner_list


def insert_to_ownedby(id_owner, id_pokemon):
    for id_ in id_owner:
        try:
            with connection.cursor() as cursor:
                query = 'INSERT into ownedby (trainer_id, pokemon_id) values ({}, {})'.format(id_, id_pokemon)
                cursor.execute(query)
                connection.commit()
        except:
            print("Error in insert_to_ownedby")


def insert_to_type_of(id_pokemon, id_type_list):
    try:
        with connection.cursor() as cursor:
            
            for id_type in id_type_list:
                query = 'INSERT into typeOf (type_id, pokemon_id) values ({}, {})'.format(id_type, id_pokemon)
                cursor.execute(query)
                connection.commit()
    except:
        print("Error in insert_to_type_of")


def insert_to_tables(pokemon_data):
    id_type = insert_to_pokemon_type(pokemon_data["type"])
    insert_to_pokemon(pokemon_data["id"], pokemon_data["name"], pokemon_data["height"], pokemon_data["weight"])
    trainers_id = insert_to_trainer(pokemon_data["ownedBy"])
    insert_to_ownedby(trainers_id, pokemon_data["id"])
    insert_to_type_of(pokemon_data["id"],[id_type])
    

def insert_to_tables2(pokemon_data):
    id_type = list()

    for type_ in pokemon_data["type"]:
        insert_to_pokemon_type(type_)
        id_type.append(type_)

    insert_to_pokemon(pokemon_data["id"], pokemon_data["name"], pokemon_data["height"], pokemon_data["weight"])
    trainers_id = insert_to_trainer(pokemon_data["ownedBy"])
    insert_to_ownedby(trainers_id, pokemon_data["id"])
    insert_to_type_of(pokemon_data["id"],id_type)
    

def insert_to_tables_from_json():
    with open("poke_data.json") as poke_json:
        poke_data = json.load(poke_json)

        for poke in poke_data:
            insert_to_tables(poke)

