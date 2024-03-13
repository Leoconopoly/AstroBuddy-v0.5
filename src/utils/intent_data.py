import json

def load_intents(json_files):
    """
    Load intents data from JSON files.

    Parameters:
        json_files (list): List of file paths to JSON files.

    Returns:
        dict: Dictionary containing loaded intents data.
    """
    intents_data = {'intents': []}
    for file_path in json_files:
        with open(file_path, 'r') as file:
            data = json.load(file)
            intents_data['intents'].extend(data['intents'])
    return intents_data
