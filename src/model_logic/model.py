import torch
import torch.nn as nn

class LSTMNet(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_size, output_size, num_layers, dropout_rate):
        """
        Initialize the LSTM network.

        Parameters:
            vocab_size (int): Size of the vocabulary.
            embedding_dim (int): Dimension of word embeddings.
            hidden_size (int): Number of features in the hidden state of the LSTM.
            output_size (int): Number of output classes.
            num_layers (int): Number of recurrent layers.
            dropout_rate (float): Dropout probability.
        """
        super(LSTMNet, self).__init__()
        # Embedding layer
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        # LSTM layer
        self.lstm = nn.LSTM(embedding_dim, hidden_size, num_layers, batch_first=True, dropout=dropout_rate)
        # Fully connected layer
        self.fc = nn.Linear(hidden_size, output_size)
    
    def forward(self, x):
        """
        Forward pass of the LSTM network.

        Parameters:
            x (torch.Tensor): Input tensor.

        Returns:
            torch.Tensor: Output tensor.
        """
        # Embedding
        embedded = self.embedding(x)
        
        # Initialize hidden and cell states
        h0 = torch.zeros(self.num_layers, embedded.size(0), self.hidden_size).to(embedded.device)
        c0 = torch.zeros(self.num_layers, embedded.size(0), self.hidden_size).to(embedded.device)
      
        # Forward propagate LSTM
        out, _ = self.lstm(embedded, (h0, c0))
        
        # Decode the hidden state of the last time step
        out = self.fc(out[:, -1, :])
        return out
