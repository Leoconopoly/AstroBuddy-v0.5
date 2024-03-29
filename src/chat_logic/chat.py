import sys
import os

# Add the parent directory of 'src' to the Python path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

import random
import sqlite3
import torch
from model_logic.model import LSTMNet  
from model_logic.nltk_utils import tokenize, sentence_to_indices, pad_sequences, create_vocab

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Function to load responses from the database
def load_responses(db_path):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Fetch data from multiple tables using JOIN operations
        cursor.execute("""
        SELECT Intents.Tag, Responses.Response, ImageURL.ImageURL
        FROM Intents
        LEFT JOIN Patterns ON Intents.IntentID = Patterns.IntentID
        LEFT JOIN Responses ON Patterns.PatternID = Responses.PatternID
        LEFT JOIN ImageURL ON Intents.IntentID = ImageURL.IntentID
        """)
        data = cursor.fetchall()
    except Exception as e:
        print(f"Error loading responses from database: {e}")
    finally:
        conn.close()
    
    # Process fetched data into response and image dictionaries
    responses = {}
    images = {}
    for tag, response, image_url in data:
        if tag not in responses:
            responses[tag] = []
            images[tag] = image_url  # This assumes only one image_url per tag, which could be altered in the future
        responses[tag].append(response)
 
    return responses, images

# Path to the SQLite database
db_path = 'db/astrobuddy_v0.5.db'  

# Load responses from the database
intents_responses, images = load_responses(db_path)

# Path to the trained model file
FILE = "data.pth"
data = torch.load(FILE, map_location=device)

# Extract data from the loaded file
vocab_size = data["vocab_size"]  
embedding_dim = data["embedding_dim"]  
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]
max_len = data["max_len"]

# Initialize the LSTM model
model = LSTMNet(vocab_size, embedding_dim, hidden_size, output_size, num_layers=data['num_layers'], dropout_rate=data['dropout_rate']).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "AstroBuddy"

# Function to get response based on input message
def get_response(msg):
    # Create vocabulary and preprocess the input message
    vocab = create_vocab(all_words)
    X = sentence_to_indices(msg, vocab)
    X_padded = pad_sequences([X], max_len)
    X_tensor = torch.tensor(X_padded, dtype=torch.long).to(device)

    # Get output from the model
    output = model(X_tensor)
    _, predicted = torch.max(output, dim=1)

    # Get the tag and confidence level of the predicted response
    tag = tags[predicted.item()]
    probs = torch.softmax(output, dim=1)
    confidence = probs[0][predicted.item()].item()
    print(tag, confidence)

    # Determine the response and image URL based on confidence level and availability of responses
    if confidence > 0.75 and tag in intents_responses:
        response = random.choice(intents_responses[tag])
        # Fetch image_url for the tag. Use default if not available.
        image_url = images.get(tag, "project_media/astobuddyfullavatar.png")
    else:
        # Default response and image URL when the bot doesn't understand
        response = "I'm sorry, I do not understand. Like you, I am still learning. Can you try messaging me again in full sentences so I can try to understand a bit better..."
        image_url = "project_media/astobuddyfullavatar.png"

    return response, image_url






