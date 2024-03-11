# intent_data.py
import json

def load_intents(json_files):
    intents_data = {'intents': []}
    for file_path in json_files:
        with open(file_path, 'r') as file:
            data = json.load(file)
            intents_data['intents'].extend(data['intents'])
    return intents_data
