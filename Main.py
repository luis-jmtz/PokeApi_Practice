import requests
import pandas as pd
import json
import streamlit as st

base_url = "https://pokeapi.co/api/v2/" # saved of convenience

latest_move_version_group = "sword-shield"


def get_pokemon_info(name):
    goal_url = f"{base_url}/pokemon/{name}"
    response = requests.get(goal_url)
    if response.status_code == 200:
        print("Data Retrieved \n")
        pokemon_data = response.json() # converts response to a python dict.
        # print(pokemon_data)
        return pokemon_data
    else:
        print(f"Failed to retrieve data: {response.status_code}")

pokemon_name = "pikachu"
pokemon_info = get_pokemon_info(pokemon_name)

# with open("data.json", "w") as f:
#     json.dump(pokemon_info, f, indent=4)




# -------------- Testing ------------------------------#

# print(type(pokemon_info["moves"])) # list
# print(type(pokemon_info["moves"][0])) # dictionary
# print(pokemon_info["moves"][0].keys())
# print(pokemon_info["moves"][0]["move"]["name"]) # gets the actual name of the move
# print(pokemon_info["moves"][0]["version_group_details"][4])

# print(len(pokemon_info["moves"][0]["version_group_details"][0]))

for version in pokemon_info["moves"][0]["version_group_details"]:
    
    version_group = version["version_group"]["name"]

    if version_group == latest_move_version_group:
        print(version_group)
