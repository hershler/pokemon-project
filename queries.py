import pymysql


connection = pymysql.connect(
    host="localhost",
    user="root",
    password="1",
    db="pokemon",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)


def findRoster(owner_name):
    with connection.cursor() as cursor:
        query = "select t_id from trainer where t_name = '{}'".format(owner_name)
        cursor.execute(query)
        owner_id = cursor.fetchall()

        query = "select pokemon_id from ownedby where trainer_id = '{}'".format(owner_id[0]['t_id'])
        cursor.execute(query)
        pokemon_id = cursor.fetchall()
        
        pokemon_list = set()

        for pokemon in pokemon_id:
            query = "select p_name from pokemon where p_id = {}".format(pokemon['pokemon_id'])
            cursor.execute(query)
            pokemon_name = cursor.fetchall()
            pokemon_list.add(pokemon_name[0]['p_name'])
    
    return pokemon_list


print(findRoster("Loga"))

def findOwners(pokemon_name):
    with connection.cursor() as cursor:
        query = "select p_id from pokemon where p_name = '{}'".format(pokemon_name)
        cursor.execute(query)
        pocemon_id = cursor.fetchall()

        query = "select trainer_id from ownedby where pokemon_id = '{}'".format(pocemon_id[0]['p_id'])
        cursor.execute(query)
        owner_id = cursor.fetchall()
        
        owner_list = set()

        for owner in owner_id:
            query = "select t_name from trainer where t_id = {}".format(owner['trainer_id'])
            cursor.execute(query)
            owner_name = cursor.fetchall()
            owner_list.add(owner_name[0]['t_name'])
    
    return owner_list

print(findOwners("gengar"))