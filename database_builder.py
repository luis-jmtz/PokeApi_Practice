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





is_name_present_script = """
SELECT * FROM Pokemon
WHERE name = ?
"""
# use the question mark to prevent injection
def is_pokemon_in_database(pokemon_name): # takes the pokemon name string
    cursor.execute(is_name_present_script, (pokemon_name,))
    result = cursor.fetchone() # fetchone() returns A row/tuple containing the column values
    return result is not None # returns true if result is not empty


# print(is_pokemon_in_database("bulbasaur"))


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




call_limit = 100
# 1025 is max value since all values after are specific forms which are outside of the scope of this project

first_100 = fr"https://pokeapi.co/api/v2/pokemon?limit={call_limit}" # gets the first 100 pokemon

response = requests.get(first_100).json()

# print(type(response))
# print(response.keys())

# print(response["results"])

# print(response["results"][0]["name"]) # prints bulbasaur

temp_name = response["results"][2]["name"]

print(temp_name)

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

poke_info = get_pokemon_info(temp_name)


print(poke_info.keys())
print(poke_info["types"]) # types is a list of dictionaries, so if the length is 1, it's monotype
print(poke_info["types"][0]["type"]["name"]) # gets the first type
# print(poke_info["types"][1]["type"]["name"]) # if no 2nd type returns an error


loop_count = 0

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


connection.commit()
cursor.close()