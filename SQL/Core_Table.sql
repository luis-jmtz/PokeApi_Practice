-- SQLite
CREATE TABLE Pokemon(
ID Integer PRIMARY KEY NOT NULL,
name Text UNIQUE NOT NULL,
dex_number Integer Not Null,
type_1 Integer Not NULL,
type_2 Integer,
sprite_link Text,
FOREIGN KEY (type_1) REFERENCES Types (ID),
FOREIGN KEY (type_2) REFERENCES Types (ID)
)
-- dex_number is pokemon_info["id"]