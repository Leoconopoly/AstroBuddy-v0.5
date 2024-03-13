import nltk
import numpy as np
from nltk.stem.porter import PorterStemmer

# Check if 'punkt' package is already downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

stemmer = PorterStemmer()

def tokenize(sentence):
    """
    Tokenize a sentence into words.

    Parameters:
        sentence (str): Input sentence.

    Returns:
        list: List of tokens.
    """
    return nltk.word_tokenize(sentence)


def stem(word):
    """
    Perform stemming on a word.

    Parameters:
        word (str): Input word.

    Returns:
        str: Stemmed word.
    """
    return stemmer.stem(word.lower())

# Function to create a word index mapping
def create_vocab(all_words):
    """
    Create a word index mapping.

    Parameters:
        all_words (list): List of all words.

    Returns:
        dict: Vocabulary mapping words to indices.
    """
    # Ensure all words are stemmed
    all_words = [stem(w) for w in all_words]
    all_words = sorted(set(all_words))  # Sort and remove duplicates to create a consistent vocabulary
    vocab = {word: i for i, word in enumerate(all_words, 1)}  # Starting index at 1 for actual words
    vocab['<PAD>'] = 0  # PAD token at index 0
    vocab['<UNK>'] = len(vocab)  # UNK token at the last index
    return vocab


# Function to convert sentences to a sequence of indices
def sentence_to_indices(sentence, vocab):
    """
    Convert sentences to a sequence of indices based on the vocabulary.

    Parameters:
        sentence (str): Input sentence.
        vocab (dict): Vocabulary mapping words to indices.

    Returns:
        list: List of indices.
    """
    tokens = tokenize(sentence)
    indices = [vocab.get(stem(token), vocab['<UNK>']) for token in tokens]  # Use vocab['<UNK>'] for OOV words
    return indices

# Function to pad sequences
def pad_sequences(sequences, max_len):
    """
    Pad sequences to a fixed length.

    Parameters:
        sequences (list): List of sequences.
        max_len (int): Maximum length to pad sequences to.

    Returns:
        np.ndarray: Padded sequences.
    """
    padded_sequences = np.zeros((len(sequences), max_len), dtype=int)
    for i, seq in enumerate(sequences):
        if len(seq) > max_len:
            padded_sequences[i, :] = seq[:max_len]
        else:
            padded_sequences[i, :len(seq)] = seq
    return padded_sequences



