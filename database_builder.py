import sqlite3

# connect to database
connection = sqlite3.connect("PokeBase.db")

# initialize cursor to interact with database
cursor = connection.cursor()





"""
# --------- Intialize Type Table -------- #
"""
with open("SQL\Types_Table.sql", 'r') as file:
    init_types_text = file.read()

cursor.execute(init_types_text)

cursor.close()