import sqlite3
import os

def db_exists(db_path):
    return os.path.exists(db_path)

def create_database_if_not_exists(db_path):
    if not db_exists(db_path):
        conn = sqlite3.connect(db_path)
        conn.close()
        print(f"Database created at {db_path}")

def clear_data_from_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Responses")
    cursor.execute("DELETE FROM Patterns")
    cursor.execute("DELETE FROM Intents")
    cursor.execute("DELETE FROM ImageURL")

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
            pattern_id = cursor.lastrowid
            
            for response in intent['responses']:
                cursor.execute("INSERT INTO Responses (PatternID, Response) VALUES (?, ?)", (pattern_id, response))
                response_id = cursor.lastrowid

        if 'image_url' in intent:
            image_url = intent['image_url'][0]
            cursor.execute("INSERT INTO ImageURL (IntentID, ImageURL) VALUES (?, ?)", (intent_id, image_url))
    
    conn.commit()
    conn.close()
