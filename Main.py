import streamlit as st
import sqlite3

st.set_page_config(page_title="Pokédex Search", page_icon="🔍")

@st.cache_resource
def get_connection():
    return sqlite3.connect("PokeBase.db", check_same_thread=False)

conn = get_connection()
cursor = conn.cursor()

@st.cache_data
def get_all_pokemon_names():
    cursor.execute("SELECT name FROM Pokemon ORDER BY dex_number")
    return [row[0] for row in cursor.fetchall()]

def get_pokemon_details(name):
    query = """
        SELECT 
            p.name,
            p.dex_number,
            t1.name AS type1,
            t2.name AS type2,
            p.sprite_link
        FROM Pokemon p
        LEFT JOIN Types t1 ON p.type_1 = t1.id
        LEFT JOIN Types t2 ON p.type_2 = t2.id
        WHERE p.name = ?
    """
    cursor.execute(query, (name,))
    row = cursor.fetchone()
    if row:
        return {
            "name": row[0],
            "dex_number": row[1],
            "type1": row[2],
            "type2": row[3] if row[3] != "None" else None,
            "sprite_link": row[4]
        }
    return None

st.title("🔍 Pokédex Search")
st.markdown("Search for a Pokémon and view its sprite and database info.")

try:
    pokemon_names = get_all_pokemon_names()
except sqlite3.OperationalError:
    st.error("Database tables not found. Please run `database_builder.py` first.")
    st.stop()

selected_pokemon = st.selectbox("Choose a Pokémon:", pokemon_names)

if selected_pokemon:
    details = get_pokemon_details(selected_pokemon)
    if details:
        col1, col2 = st.columns([1, 2])
        with col1:
            if details["sprite_link"]:
                st.image(details["sprite_link"], width=200, caption=details["name"].capitalize())
            else:
                st.warning("No sprite available.")
        with col2:
            st.subheader(details["name"].capitalize())
            st.write(f"**National Dex Number:** #{details['dex_number']:03d}")
            type_str = details["type1"].capitalize()
            if details["type2"]:
                type_str += f" / {details['type2'].capitalize()}"
            st.write(f"**Type(s):** {type_str}")
    else:
        st.error(f"Pokémon '{selected_pokemon}' not found.")