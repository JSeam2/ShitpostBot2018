import torch
import os
import argparse
import string
import random

from models_rnn import *
from utils import *

def generate(decoder,
             prime_str="A",
             predict_len=100,
             temperature=0.8,
             cuda=False):
    hidden = decoder.init_hidden(1)
    prime_input = Variable(char_tensor(prime_str).unsqueeze(0))

    if cuda:
        hidden = hidden.cuda()
        prime_input = prime_input.cuda()

    predicted = prime_str

    for p in range(len(prime_str) - 1):
        _, hidden = decoder(prime_input[:,p], hidden)

    inp = prime_input[:,-1]

    for p in range(predict_len):
        output, hidden = decoder(inp, hidden)

        output_dist = output.data.view(-1).div(temperature).exp()

        top_i = torch.multinomial(output_dist, 1)[0]

        predicted_char = all_characters[top_i]
        predicted += predicted_char

        inp = Variable(char_tensor(predicted_char).unsqueeze(0))

        if cuda:
            inp = inp.cuda()

    return predicted
