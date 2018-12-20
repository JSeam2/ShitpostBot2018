import os
from io import open
import torch
import pickle


class Dictionary(object):
    """
    Dictionary class for rnn
    """
    def __init__(self):
        self.word2idx = {}
        self.idx2word = []

    def add_word(self, word):
        """
        Adds word to dictionary
        """
        if word not in self.word2idx:
            self.idx2word.append(word)
            self.word2idx[word] = len(self.idx2word) - 1

        return self.word2idx[word]

    def __len__(self):
        return len(self.idx2word)


class Corpus(object):
    """
    Tokenize the pkl file of text information
    """
    def __init__(self, data_path='data.pkl', split=[0.6, 0.2, 0.2]):
        """
        Initialize Corpus

        Args:
            data_path: String, path to pickled data file
            split: List of Float, Train, Valid, Test Split
        """
        self.dictionary = Dictionary()

        assert os.path.isfile(data_path)

        # Load data
        with open(data_path, "rb") as f:
            self.data = pickle.load(f)

        # Split data
        self.train_size = int(round(split[0] * len(self.data)))
        self.valid_size = int(round(split[1] * len(self.data)))
        self.test_size = int(round(split[2] * len(self.data)))
        self.train = self.tokenize(self.data[0:self.train_size])
        self.valid = self.tokenize(
            self.data[self.train_size:self.train_size + self.valid_size])
        self.test = self.tokenize(
            self.data[self.train_size + self.valid_size:
                      self.train_size + self.valid_size + self.test_size])

    def tokenize(self, str_list):
        """
        Tokenize the list of strings
        """
        # Add word to dictionary
        # Tokenize List
        tokens = 0
        for line in str_list:
            words = line.split() + ['<eos>']
            tokens += len(words)

            for word in words:
                # populate dictionary
                self.dictionary.add_word(word)


        token_num = 0
        ids = torch.LongTensor(tokens)
        for line in str_list:
            words = line.split() + ['<eos>']

            for word in words:
                # tokenize contents
                ids[token_num] = self.dictionary.word2idx[word]
                token_num += 1

        return ids


