# For Future Development and Use

import json
import requests

def load_api_key(filepath):
    with open(filepath, 'r') as file:
        config = json.load(file)
        return config.get('api_key')

def search_nasa_media(query, api_key):
    url = f"https://images-api.nasa.gov/search?q={query}&media_type=image"
    headers = {'Authorization': api_key}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if 'collection' in data and 'items' in data['collection']:
            items = data['collection']['items']
            if items:
                # Return the URL of the first image found
                return items[0]['links'][0]['href']
    else:
        print("Error:", response.status_code, response.text)  # Print the error code and message

    return None

if __name__ == "__main__":
    # Load API key from configuration file
    api_key = load_api_key('config.json')
    if api_key is None:
        print("Error: API key not found in the configuration file.")
    else:
        # Example usage:
        query = 'earth'
        image_url = search_nasa_media(query, api_key)
        if image_url:
            print("Here's an image related to your query:", image_url)
        else:
            print("No image found for the given query.")




