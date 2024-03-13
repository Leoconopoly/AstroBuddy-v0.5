import sqlite3
from nltk_utils import tokenize, create_vocab, sentence_to_indices, pad_sequences
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from model import LSTMNet  # Updated LSTM model

# Database connection and data loading
def load_data_from_db(db_path):
    """
    Load data from the SQLite database.

    Parameters:
        db_path (str): Path to the SQLite database file.

    Returns:
        list: List of tuples containing patterns and corresponding tags.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT Patterns.Pattern, Intents.Tag FROM Patterns JOIN Intents ON Patterns.IntentID = Intents.IntentID")
    data = cursor.fetchall()
    conn.close()
    return data

class ChatDataset(Dataset):
    def __init__(self, x_train, y_train):
        self.n_samples = len(x_train)
        self.x_data = x_train
        self.y_data = y_train

    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]
    
    def __len__(self):
        return self.n_samples

def main():
    db_path = 'db/astrobuddy_v0.5.db'
    data = load_data_from_db(db_path)
    
    all_words = []
    tags = []
    xy = []
    for pattern, tag in data:
        tags.append(tag)
        xy.append((pattern, tag))

    # Correction starts here
    ignore_words = ['?', '!', '.', ',']
    # Correctly tokenize and filter the patterns before extending all_words
    all_words = [token for pattern, tag in data for token in tokenize(pattern) if token not in ignore_words]
    all_words = sorted(set(all_words))  # Deduplicate and sort
    tags = sorted(set(tags))

    vocab = create_vocab(all_words)
    vocab_size = len(vocab)  # Size of vocabulary
    embedding_dim = 100  
    hidden_size = 64  
    output_size = len(tags)
    num_layers = 2  # LSTM layers
    dropout_rate = 0.5

    # Preparing sequences and labels
    sequences = [sentence_to_indices(pattern, vocab) for pattern, _ in xy]
    max_len = max(len(seq) for seq in sequences)
    padded_sequences = pad_sequences(sequences, max_len)

    labels = torch.tensor([tags.index(tag) for _, tag in xy])

    x_train = torch.tensor(padded_sequences, dtype=torch.long)
    y_train = labels

    dataset = ChatDataset(x_train, y_train)
    train_loader = DataLoader(dataset=dataset, batch_size=8, shuffle=True)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = LSTMNet(vocab_size, embedding_dim, hidden_size, output_size, num_layers, dropout_rate).to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    # Training loop
    for epoch in range(1000):
        for (words, labels) in train_loader:
            words = words.to(device)
            labels = labels.to(device)

            output = model(words)
            loss = criterion(output, labels)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        if (epoch + 1) % 100 == 0:
            print(f'Epoch {epoch+1}/1000, Loss: {loss.item():.4f}')

    print(f'Final Loss: {loss.item():.4f}')

    # Save the model state
    FILE = "data.pth"
    torch.save({
        "model_state": model.state_dict(),
        "vocab_size": vocab_size,  # Added vocab_size for embedding layer
        "embedding_dim": embedding_dim,  # Added embedding_dim
        "hidden_size": hidden_size,
        "output_size": output_size,
        "num_layers": num_layers,  # Good practice to save the number of layers
        "dropout_rate": dropout_rate,  # Saving dropout_rate might be useful for model reloading
        "all_words": all_words,  
        "tags": tags,
        "max_len": max_len  # Save the max_len for padding sequences
    }, FILE)

    print(f'training complete. file saved to {FILE}')


if __name__ == '__main__':
    main()

