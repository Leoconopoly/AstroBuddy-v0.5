import sqlite3
import os
import logging
from logging.handlers import RotatingFileHandler
import time
import uuid

class DBShutdownFileHandler(RotatingFileHandler):
    def __init__(self, filename, db_path='log_data/chat_logs.db'):
        super().__init__(filename, maxBytes=0, backupCount=0)
        self.db_path = db_path
        self.ensure_db_directory()
        self.conversation_id = str(uuid.uuid4())  # Generate a unique conversation ID

    def close(self):
        self.transferLogToDB(self.baseFilename)
        open(self.baseFilename, 'w').close()
        super().close()

    def transferLogToDB(self, log_file_path):
        retries = 5
        while retries > 0:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute('''CREATE TABLE IF NOT EXISTS chat_logs 
                                (conversation_id TEXT, timestamp TEXT, user_message TEXT, bot_response TEXT)''')
                with open(log_file_path, 'r') as file:
                    print("Opened log file")  # Debug print
                    for line in file.readlines():
                        log_entry = self.parse_log_entry(line)
                        if log_entry is not None:
                            timestamp, user_message, bot_response = log_entry
                            cursor.execute('INSERT INTO chat_logs (conversation_id, timestamp, user_message, bot_response) VALUES (?, ?, ?, ?)', 
                                        (self.conversation_id, timestamp, user_message, bot_response))
                conn.commit()
                conn.close()
                break  # Exit loop if operation is successful
            except sqlite3.OperationalError as e:
                if "locked" in str(e):
                    retries -= 1
                    time.sleep(1)  # Wait a bit for the lock to clear
                else:
                    raise  # Re-raise exception if it's not a lock-related error


    def ensure_db_directory(self):
        db_dir = os.path.dirname(self.db_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)

    def parse_log_entry(self, log_entry):
        try:
            parts = log_entry.split(' - ', 1)
            if len(parts) < 2:
                raise ValueError("Log entry does not have the expected format")

            timestamp_part = parts[0]
            message_part = parts[-1]

            # Check if the message part contains the expected format
            if '|' not in message_part:
                # Skip processing this log entry
                return None

            message_split = message_part.split(' | AstroBuddy: ')
            if len(message_split) != 2:
                raise ValueError("Message part does not have the expected format after splitting")

            user_message = message_split[0].split(': ')[1].strip()
            bot_response = message_split[1].strip()

            return timestamp_part, user_message, bot_response
        except Exception as e:
            print(f"Error parsing log entry: {log_entry} | Error: {e}")
            logger.error(f"Error parsing log entry: {log_entry} | Error: {e}")  # Log error message
            return None







logger = logging.getLogger('AstroBuddyLogger')
logger.setLevel(logging.INFO)
handler = DBShutdownFileHandler('log_data/astrobuddy_chat_logs.log')
handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s', '%Y-%m-%d %H:%M:%S'))
logger.addHandler(handler)
