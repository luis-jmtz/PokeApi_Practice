import requests
import pandas as pd
import streamlit as st

base_url = "https://pokeapi.co/api/v2/" # saved of convenience

def get_pokemon_info(name):
    goal_url = f"{base_url}/pokemon/{name}"
    response = requests.get(goal_url)
    if response.status_code == 200:
        print("Data Retrieved")
        pokemon_data = response.json() # converts response to a python dict.
        # print(pokemon_data)
        return pokemon_data
    else:
        print(f"Failed to retrieve data: {response.status_code}")

# pokemon_name = "pikachu"
# pokemon_info = get_pokemon_info(pokemon_name)

# if pokemon_info:
#     print(pokemon_info["name"])
#     print(pokemon_info["id"])