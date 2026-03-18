import sqlite3
import requests
import json

# connect to database
connection = sqlite3.connect("PokeBase.db")

# initialize cursor to interact with database
cursor = connection.cursor()

connection.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints

# base url for api
base_url = "https://pokeapi.co/api/v2/"








call_limit = 50
# 1025 is max value since all values after are specific forms which are outside of the scope of this project

raw_response = fr"https://pokeapi.co/api/v2/pokemon?limit={call_limit}" # gets the first 100 pokemon

response = requests.get(raw_response).json()

# temp_name = response["results"][2]["name"]


# Functions that extract the pokemon values

# ------------------------------------------------------------------- #

def get_pokemon_info(name):
    goal_url = f"{base_url}/pokemon/{name}"
    response = requests.get(goal_url)
    if response.status_code == 200:
        # print("Data Retrieved \n")
        pokemon_data = response.json() # converts response to a python dict.
        # print(pokemon_data)
        return pokemon_data
    else:
        print(f"Failed to retrieve data: {response.status_code}")

# poke_info = get_pokemon_info(temp_name)



type_conversion_script = """
Select * FROM Types
WHERE name = ?
"""

def convert_type_to_id(poke_type):
    cursor.execute(type_conversion_script, (poke_type,))
    result = cursor.fetchone()
    # print(result[0])
    type_id =  result[0]
    return type_id


# convert_type_to_id("fire")


def extract_pokemon_values(poke_info):
    poke_name = poke_info["name"]
    dex_number = poke_info["id"]
    sprite_link = poke_info["sprites"]["front_default"]

    types_list = poke_info["types"]
    type1 = types_list[0]["type"]["name"] # pokemon's first type
    

    if len(types_list) == 1:
        # if a pokemon is monotype
        type2 = "None"
    else:
        type2 = types_list[1]["type"]["name"]

    # print(f"Type 1: {type1}")
    # print(f"type 2: {type2}")

    type_id_1 = convert_type_to_id(type1)
    type_id_2 = convert_type_to_id(type2)


    # print(f"Name: {poke_name}")
    # print(f"Dex Number: {dex_number}")
    # print(f"Type 1 id: {type_id_1}")
    # print(f"Type 2 id: {type_id_2}")
    # print(f"Sprite Link: {sprite_link}")
    return [poke_name, dex_number, type_id_1, type_id_2, sprite_link]



# ------------------------------------------------------------------- #


# Actually updates table

is_name_present_script = """
SELECT * FROM Pokemon
WHERE name = ?
"""
# use the question mark to prevent injection
def is_pokemon_in_database(pokemon_name): # takes the pokemon name string
    cursor.execute(is_name_present_script, (pokemon_name,))
    result = cursor.fetchone() # fetchone() returns A row/tuple containing the column values
    return result is not None # returns true if result is not empty



update_entry_string = '''
Update Pokemon
SET dex_number = ?, type1 = ?, type2 = ?, sprite_link = ?
WHERE name = ?
'''

def update_entry(pokemon_name):
    '''
    if a pokemon is already in the database, this function will update it to match the 
    latest version in the api instead of creating a new entry.
    '''
    pass



def update_pokemon_table():
    loop_count = 0
    
    while loop_count < call_limit:
        try:
            poke_name = response["results"][loop_count]["name"]
            print(poke_name)

            poke_info = get_pokemon_info(poke_name)
            poke_values = extract_pokemon_values(poke_info)

            if is_pokemon_in_database(poke_name):
                pass
            else:
                update_entry(poke_name)

        except:
            print("Loop Ends")
            break



        loop_count += 1


update_pokemon_table()


# while loop_count < call_limit:
#     # try-catch keeps code from encountering an "index out of bounds" problem
#     try:
#         print(response["results"][loop_count]["name"]) # loop count is the index of the result, name is the key for the value
#         # print(f"Loop: {loop_count}")
#     except:
#         print("Loop ends")
#         break

#     loop_count += 1




# ------------- Initialize Core Table ----------- #
'''
# with open("SQL\Core_Table.sql", "r") as file:
#     init_core_table = file.read()

# cursor.execute(init_core_table)
'''



# --------- Initialize Type Table -------- #

'''
# with open("SQL\Types_Table.sql", 'r') as file:
#     init_types_text = file.read()

# cursor.execute(init_types_text)


# getting the pokemon types
response = requests.get("https://pokeapi.co/api/v2/type")
types_dict = response.json() # converts response to a python dict.

# print(types_dict["results"]) # list of dicts with type information

types_list = []

for x in types_dict["results"]:
    # print(x["name"])
    types_list.append(x["name"])

print(types_list)

# add types to sql database

for x in types_list:
    sql_string = f"Insert Into Types (name) Values ('{x}');"
    cursor.execute(sql_string)
'''

# cursor.execute("Insert Into Types (name) Values ('None');")


connection.commit()
cursor.close()