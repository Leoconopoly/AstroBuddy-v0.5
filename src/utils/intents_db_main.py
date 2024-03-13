from intents_db import create_database_if_not_exists, insert_data_to_db
from intent_data import load_intents

if __name__ == "__main__":
    # List of paths to JSON files containing intents data
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
    
    # Path to the SQLite database
    db_path = 'db/astrobuddy_v0.5.db'  
    
    # Create the database if it doesn't exist
    create_database_if_not_exists(db_path)
    
    # Load intents data from JSON files
    intents_data = load_intents(json_files)
    
    # Insert the loaded intents data into the database
    insert_data_to_db(intents_data, db_path)

