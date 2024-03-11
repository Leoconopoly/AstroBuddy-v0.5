import json
import sqlite3
import os

def db_exists(db_path):
    """
    Check if the database file exists.

    Parameters:
        db_path (str): Path to the SQLite database file.

    Returns:
        bool: True if the database file exists, False otherwise.
    """
    return os.path.exists(db_path)

def create_database_if_not_exists(db_path):
    """
    Create a new SQLite database if it doesn't exist.

    Parameters:
        db_path (str): Path to the SQLite database file.
    """
    if not db_exists(db_path):
        conn = sqlite3.connect(db_path)
        conn.close()
        print(f"Database created at {db_path}")

def load_intents(json_files):
    """
    Load intents data from JSON files.

    Parameters:
        json_files (list): List of paths to JSON files containing intent data.

    Returns:
        dict: Dictionary containing loaded intent data.
    """
    intents_data = {'intents': []}
    for file_path in json_files:
        with open(file_path, 'r') as file:
            data = json.load(file)
            intents_data['intents'].extend(data['intents'])
    return intents_data

def clear_data_from_db(db_path):
    """
    Clear data from all tables in the database.

    Parameters:
        db_path (str): Path to the SQLite database file.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Responses")
    cursor.execute("DELETE FROM Patterns")
    cursor.execute("DELETE FROM Intents")
    cursor.execute("DELETE FROM ImageURL")  # Clear ImageURL table

    conn.commit()
    conn.close()

def create_db_schema(db_path):
    """
    Create the database schema if it doesn't exist.

    Parameters:
        db_path (str): Path to the SQLite database file.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Intents (
        IntentID INTEGER PRIMARY KEY AUTOINCREMENT,
        Tag TEXT UNIQUE NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Patterns (
        PatternID INTEGER PRIMARY KEY AUTOINCREMENT,
        IntentID INTEGER NOT NULL,
        Pattern TEXT NOT NULL,
        FOREIGN KEY (IntentID) REFERENCES Intents(IntentID)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Responses (
        ResponseID INTEGER PRIMARY KEY AUTOINCREMENT,
        PatternID INTEGER NOT NULL,
        Response TEXT NOT NULL,
        FOREIGN KEY (PatternID) REFERENCES Patterns(PatternID)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ImageURL (
        ImageID INTEGER PRIMARY KEY AUTOINCREMENT,
        IntentID INTEGER NOT NULL,
        ImageURL TEXT,
        FOREIGN KEY (IntentID) REFERENCES Intents(IntentID)
    )
    """)

    conn.commit()
    conn.close()

def insert_data_to_db(data, db_path):
    """
    Insert data into the database.

    Parameters:
        data (dict): Intent data to be inserted into the database.
        db_path (str): Path to the SQLite database file.
    """
    create_db_schema(db_path)
    clear_data_from_db(db_path)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for intent in data['intents']:
        try:
            cursor.execute("INSERT INTO Intents (Tag) VALUES (?)", (intent['tag'],))
            conn.commit()  
        except sqlite3.IntegrityError:
            print(f"Duplicate tag found: {intent['tag']}")
            continue  

        intent_id = cursor.lastrowid

        for pattern in intent['patterns']:
            cursor.execute("INSERT INTO Patterns (IntentID, Pattern) VALUES (?, ?)", (intent_id, pattern))
            pattern_id = cursor.lastrowid # Capture the PatternID here
            
            for response in intent['responses']:
                cursor.execute("INSERT INTO Responses (PatternID, Response) VALUES (?, ?)", (pattern_id, response))
                response_id = cursor.lastrowid  # Capture the ResponseID here

        # Check if image_url is present in the intent
        if 'image_url' in intent:
            image_url = intent['image_url'][0]
            cursor.execute("INSERT INTO ImageURL (IntentID, ImageURL) VALUES (?, ?)", (intent_id, image_url))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Paths to JSON files
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