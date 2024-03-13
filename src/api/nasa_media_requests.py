# For future development, we will use the NASA API to search for images related to a given query.
# Importing necessary libraries
import json
import requests

# Function to load API key from a JSON configuration file
def load_api_key(filepath):
    # Open the JSON configuration file
    with open(filepath, 'r') as file:
        # Load the JSON content
        config = json.load(file)
        # Extract and return the API key from the configuration
        return config.get('api_key')

# Function to search NASA media for a given query
def search_nasa_media(query, api_key):
    # Construct the URL for the API request
    url = f"https://images-api.nasa.gov/search?q={query}&media_type=image"
    # Set up headers with API key for authentication
    headers = {'Authorization': api_key}

    # Send GET request to NASA API
    response = requests.get(url, headers=headers)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse response JSON data
        data = response.json()
        # Check if 'collection' and 'items' are present in the response
        if 'collection' in data and 'items' in data['collection']:
            # Extract 'items' list from response
            items = data['collection']['items']
            # Check if there are any items in the response
            if items:
                # Return the URL of the first image found
                return items[0]['links'][0]['href']
    else:
        # Print error message if request was not successful
        print("Error:", response.status_code, response.text)  # Print the error code and message

    # Return None if no image URL was found
    return None

# Entry point of the script
if __name__ == "__main__":
    # Load API key from configuration file
    api_key = load_api_key('config.json')
    # Check if API key was successfully loaded
    if api_key is None:
        print("Error: API key not found in the configuration file.")
    else:
        # Example usage:
        query = 'earth'  # Define the search query
        # Call the function to search NASA media with the provided query and API key
        image_url = search_nasa_media(query, api_key)
        # Check if an image URL was returned
        if image_url:
            print("Here's an image related to your query:", image_url)
        else:
            print("No image found for the given query.")




