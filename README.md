# Pokédex Search App

A lightweight Pokédex app that allows users to search for Pokémon by name and view their sprite, National Pokédex number, and types. Data is fetched from the [PokeAPI](https://pokeapi.co/) and stored locally in an SQLite database for fast offline-like access. The frontend is built with [Streamlit](https://streamlit.io/).

## Features

- Search for any of the first 1025 Pokémon (up to current generation limits).
- View Pokémon sprite, National Dex number, and type(s).
- Data is automatically updated from the PokeAPI when `database_builder.py` is run.
- Simple, responsive UI built with Streamlit.

## Project Structure
.  
├── database\_builder.py # Fetches Pokémon data from PokeAPI and populates SQLite DB  
├── Main.py # Streamlit web application  
├── Core\_Table.sql # SQL schema for the Pokemon table  
├── Types\_Table.sql # SQL schema for the Types table  
└── PokeBase.db # SQLite database (generated after running database\_builder.py)



## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/luis-jmtz/PokeApi_Practice
   cd pokedex-search
   ```


2. **Install required packages**
    ```python
    pip install streamlit requests
    ```

## How It Works

-   **database\_builder.py**
    
    -   Fetches a list of Pokémon names from `https://pokeapi.co/api/v2/pokemon?limit=1025`.
    -   For each name, retrieves detailed info (ID, types, sprite URL).
    -   Converts type names to their corresponding IDs from the `Types` table.
    -   Inserts new records or updates existing ones in the `Pokemon` table.
-   **Main.py (Streamlit frontend)**
    
    -   Connects to `PokeBase.db`.
    -   Caches Pokémon names and database connection for performance.
    -   Uses a `LEFT JOIN` with the `Types` table to display type names instead of IDs.
    -   Displays sprite image and Pokémon details.
-   **SQL Schema**
    
    -   `Types`: stores type names with auto-incrementing IDs.
    -   `Pokemon`: stores each Pokémon's name, National Dex number, type IDs (foreign keys), and sprite URL.

## Dependencies

-   [Streamlit](https://streamlit.io/) – for the web interface.
-   [Requests](https://docs.python-requests.org/) – for calling the PokeAPI.
-   Python standard libraries: `sqlite3`, `json`.

## Limitations & Future Improvements

-   Only the first 1025 Pokémon are included (up to a certain generation). Forms, gigantamax, or alternate forms are excluded.
-   API calls are sequential; could be parallelized to speed up database building.
-   No caching of API responses – each run rebuilds the database from scratch (but updates existing entries without duplication).
-   The app does not support searching by type or other filters yet.