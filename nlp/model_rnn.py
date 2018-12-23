import torch.nn as nn


class LSTMModel(nn.Module):
    def __init__(self, num_token, num_input, num_hidden, num_layer,
                 dropout=0.5):
        """
        We used an augmented LSTM model

        The layout is as follows:
            Embedding
            Dropout
            LSTM w/ relu nonlinearity and dropout
            Decoder

        We tie weights to improve the performance of the net
        """
        super(LSTMModel, self).__init__()

        self.drop = nn.Dropout(dropout)

        # Use Embedding layer to encode inputs to the neural net
        self.encoder = nn.Embedding(num_token, num_input)

        # improve rnn with relu nonlinearity
        # https://arxiv.org/pdf/1511.03771v3.pdf
        self.rnn = nn.LSTM(num_input, num_hidden, num_layer,
                           dropout=dropout)

        # Use a Linear layer as a decoder
        self.decoder = nn.Linear(num_hidden, num_token)

        # Tie weights for additional improvements
        # https://arxiv.org/abs/1611.01462
        # Make sure hidden layer size equal to input size
        assert num_hidden == num_input
        self.decoder.weight = self.encoder.weight

        self.init_weights()

        self.num_hidden = num_hidden
        self.num_layers = num_layer

    def init_weights(self):
        """
        Initialize weights
        """
        weight_range = 0.1
        self.encoder.weight.data.uniform_(-weight_range, weight_range)
        self.decoder.bias.data.zero_()
        self.decoder.weight.data.uniform_(-weight_range, weight_range)

    def forward(self, input, hidden):
        """
        Forward propagation of the model
        """
        embedding = self.drop(self.encoder(input))
        output, hidden = self.rnn(embedding, hidden)
        output = self.drop(output)
        decoded = self.decoder(output.view(output.size(0)*output.size(1),
                                           output.size(2)))
        return decoded.view(output.size(0),
                            output.size(1),
                            decoded.size(1)), hidden

    def init_hidden(self, batch_size):
        """
        Initialize hidden layers
        """
        # get weights from parameter which is a generator
        weight = next(self.parameters())
        return (weight.new_zeros(self.num_layers, batch_size, self.num_hidden),
                weight.new_zeros(self.num_layers, batch_size, self.num_hidden))


class GRUModel(nn.Module):
    def __init__(self, num_token, num_input, num_hidden, num_layer,
                 dropout=0.5):
        """
        This is similar to LSTMModel but using GRU

        The layout is as follows:
            Embedding
            Dropout
            GRU w/ relu nonlinearity and dropout
            Decoder

        We tie weights to improve the performance of the net
        """
        super(LSTMModel, self).__init__()

        self.drop = nn.Dropout(dropout)

        # Use Embedding layer to encode inputs to the neural net
        self.encoder = nn.Embedding(num_token, num_input)

        # improve rnn with relu nonlinearity
        # https://arxiv.org/pdf/1511.03771v3.pdf
        self.rnn = nn.GRU(num_input, num_hidden, num_layer,
                          dropout=dropout)

        # Use a Linear layer as a decoder
        self.decoder = nn.Linear(num_hidden, num_token)

        # Tie weights for additional improvements
        # https://arxiv.org/abs/1611.01462
        # Make sure hidden layer size equal to input size
        assert num_hidden == num_input
        self.decoder.weight = self.encoder.weight

        self.init_weights()

        self.num_hidden = num_hidden
        self.num_layers = num_layer

    def init_weights(self):
        """
        Initialize weights
        """
        weight_range = 0.1
        self.encoder.weight.data.uniform_(-weight_range, weight_range)
        self.decoder.bias.data.zero_()
        self.decoder.weight.data.uniform_(-weight_range, weight_range)

    def forward(self, input, hidden):
        """
        Forward propagation of the model
        """
        embedding = self.drop(self.encoder(input))
        output, hidden = self.rnn(embedding, hidden)
        output = self.drop(output)
        decoded = self.decoder(output.view(output.size(0)*output.size(1),
                                           output.size(2)))
        return decoded.view(output.size(0),
                            output.size(1),
                            decoded.size(1)), hidden

    def init_hidden(self, batch_size):
        """
        Initialize hidden layers
        """
        # get weights from parameter which is a generator
        weight = next(self.parameters())
        return weight.new_zeros(self.num_layers, batch_size, self.num_hidden)
