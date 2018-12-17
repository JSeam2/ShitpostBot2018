"""
models developed
"""
import math
import time
import torch
import torch.nn as nn
from torch.autograd import Variable

from utils import *


class CharLSTM(nn.Module):
    """
    Model for CharLSTM
    """
    def __init__(self, input_size, hidden_size, output_size, n_layers=1,
                 dropout=0.1):
        """
        Initial configuration

        Args:
            input_size: Int, the size of the input to the neural net
            hidden_size: Int, the size of the hidden layers
            output_size: Int, the size of the output layer
            n_layers: Int, the number of LSTM layers (default=2)
        """
        super(CharLSTM, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.n_layers = n_layers

        # Encoder > RNN > Decoder 
        # Encoder and Decoder input and output size is the ascii dim
        self.encoder = nn.Embedding(input_size, hidden_size)
        self.rnn = nn.LSTM(hidden_size, hidden_size, n_layers)
        self.dropout = nn.Dropout(0.1)
        self.decoder = nn.Linear(hidden_size, output_size)

    def forward(self, input_var, hidden):
        """
        Forward propagation of the neural network

        Args:
            input_var: Array, the input to be evaluated
            hidden: Array, the state of the hidden layer

        Returns:
            output: Array, of forward pass
            hidden: Array, of forward pass
        """
        batch_size = input_var.size(0)

        encoded = self.encoder(input_var)
        output, hidden = self.rnn(encoded.view(1, batch_size, -1), hidden)
        output = self.dropout(output)
        output = self.decoder(output.view(batch_size, -1))
        return output, hidden

    def init_hidden(self, batch_size):
        """
        Utility to initialie hidden layer with 0

        Args:
            batch_size: Int, the batch size to be used

        Returns:
            Array of 0s
        """
        return (torch.zeros(self.n_layers, batch_size, self.hidden_size),
                torch.zeros(self.n_layers, batch_size, self.hidden_size))
