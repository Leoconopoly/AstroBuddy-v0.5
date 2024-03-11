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

def load_responses(db_path):
    """
    Load responses from the database.

    Parameters:
        db_path (str): Path to the SQLite database file.

    Returns:
        dict: Dictionary containing responses grouped by tags.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
        SELECT Intents.Tag, Responses.Response
        FROM Intents
        LEFT JOIN Patterns ON Intents.IntentID = Patterns.IntentID
        LEFT JOIN Responses ON Patterns.PatternID = Responses.PatternID
        """)
        data = cursor.fetchall()
        
    except Exception as e:
        print(f"Error loading responses from database: {e}")
    finally:
        conn.close()
    
    responses = {}
    for tag, response in data:
        if tag not in responses:
            responses[tag] = []
        responses[tag].append(response)
 
    return responses

db_path = 'db/astrobuddy_v0.5.db'  
intents_responses = load_responses(db_path)

FILE = "data.pth"
data = torch.load(FILE, map_location=device)

vocab_size = data["vocab_size"]  
embedding_dim = data["embedding_dim"]  
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]
max_len = data["max_len"]

model = LSTMNet(vocab_size, embedding_dim, hidden_size, output_size, num_layers=data['num_layers'], dropout_rate=data['dropout_rate']).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "AstroBuddy"

def get_response(msg):
    """
    Get the response from the bot based on the input message.

    Parameters:
        msg (str): The input message.

    Returns:
        str: The response from the bot.
    """
    vocab = create_vocab(all_words)
    X = sentence_to_indices(msg, vocab)
    X_padded = pad_sequences([X], max_len)
    X_tensor = torch.tensor(X_padded, dtype=torch.long).to(device)

    output = model(X_tensor)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]
    probs = torch.softmax(output, dim=1)
    confidence = probs[0][predicted.item()].item()

    if confidence > 0.75 and tag in intents_responses: # Confidence rating changed from .75 to .8
        response = random.choice(intents_responses[tag])
    else:
        response = "I'm sorry I do not understand, like you I am still learning. Can you try messaging me again in full sentences so I can try to understand a bit better..."

    return response




