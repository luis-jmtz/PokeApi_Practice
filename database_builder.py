import sqlite3
import requests
import json

# connect to database
connection = sqlite3.connect("PokeBase.db")

# initialize cursor to interact with database
cursor = connection.cursor()

connection.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints





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