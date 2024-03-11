# main.py
from intents_database import create_database_if_not_exists, insert_data_to_db
from intent_data import load_intents

if __name__ == "__main__":
    json_files = [
        'data/intents_asteroidbelt.json',
        'data/intents_astrobuddyquestions.json',
        'data/intents_beyondthesolarsystem.json',
        'data/intents_dwarfplanets.json',
        'data/intents_earthandmoon.json',
        'data/intents_generalastroquestions.json',
        'data/intents_greetings.json',
        'data/intents_jupiter.json',
        'data/intents_mars.json',
        'data/intents_mercury.json',
        'data/intents_misconceptions.json',
        'data/intents_neptune.json',
        'data/intents_saturn.json',
        'data/intents_sun.json',
        'data/intents_uranus.json',
        'data/intents_venus.json'
    ]
    db_path = 'db/astrobuddy_v0.5.db'  
    create_database_if_not_exists(db_path)
    intents_data = load_intents(json_files)
    insert_data_to_db(intents_data, db_path)
