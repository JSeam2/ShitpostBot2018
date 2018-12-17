import argparse
import os
import pickle
from tqdm import tqdm

import torch
import torch.nn as nn
from torch.autograd import Variable

from utils import *
from models_rnn import *
from generate import *

# Available model types:
# --model_type char_lstm
# --model_type char_gru

# Arg parser arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("data_filename", type=str, default="data.pkl")
argparser.add_argument("--model_type", type=str, default="char_lstm")
argparser.add_argument("--epochs", type=int, default=2000)
argparser.add_argument("--print_every", type=int, default=100)
argparser.add_argument("--hidden_size", type=int, default=100)
argparser.add_argument("--n_layers", type=int, default=2)
argparser.add_argument("--learning_rate", type=float, default=0.01)
argparser.add_argument("--chunk_len", type=int, default=200)
argparser.add_argument("--batch_size", type=int, default=100)
argparser.add_argument("--shuffle", action="store_true")
argparser.add_argument("--cuda", action="store_true")

args = argparser.parse_args()

# Check if cuda is available
if args.cuda:
    print("Using CUDA")

# Open file we assume this file to be the data.pkl file containing a list of 
# strings
with open(args.data_filename, "rb") as f:
    data = pickle.load(f)


def random_training_set(chunk_len, batch_size):
    """
    Generate a random training set

    Args:
        chunk_len: Int, size of each chunk
        batch_size: Int, size of each batch
    """
    inp = torch.LongTensor(batch_size, chunk_len)
    target = torch.LongTensor(batch_size, chunk_len)

    for bi in range(batch_size):
        start_index = random.randint(0, len(data) - chunk_len)
        end_index = start_index + chunk_len + 1
        chunk = data[start_index:end_index]
        inp[bi] = char_tensor(chunk[:-1])
        target[bi] = char_tensor(chunk[1:])

    inp = Variable(inp)
    target = Variable(target)

    if args.cuda:
        inp = inp.cuda()
        target = target.cuda()

    return inp, target


def train(inp, target):
    """
    Function to train the neural net

    Args:
        inp: the input variable
        target: the target variable
    """
    hidden = decoder.init_hidden(args.batch_size)

    if args.cuda:
        hidden = hidden.cuda()

    decoder.zero_grad()
    loss = 0

    for c in range(args.chunk_len):
        output, hidden = decoder(inp[:, c], hidden)
        loss += criterion(output.view(args.batch_size, -1), target[:,c])

    # backprop
    loss.backward()

    decoder_optimizer.step()

    return loss.data[0] / args.chunk_len


def save(decoder):
    """
    Save rnn model
    """
    save_filename = os.path.splitext(os.path.basename(args.data_filename))[0] \
            + '.pt'

    torch.save(decoder.state_dict(), save_filename)

    print("Saved model as {}".format(save_filename))


# get model type and initialize model
decoder = None
if args.model_type == "char_lstm":
    decoder = CharLSTM(
        n_characters,
        args.hidden_size,
        n_characters,
        n_layers=args.n_layers,)

# Use ADAM optimizer
decoder_optimizer = torch.optim.Adam(decoder.parameters(),
                                     lr=args.learning_rate)

# Use CrossEntropy to Optimize
criterion = nn.CrossEntropyLoss()

if args.cuda:
    decoder.cuda()

start = time.time()
all_losses = []
loss_avg = 0

try:
    print("Training for {} epochs".format(args.epochs))

    for epoch in tqdm(range(1, args.epochs + 1)):
        loss = train(*random_training_set(args.chunk_len, args.batch_size))
        loss_avg += loss

        if epoch % args.print_every == 0:
            print("[{} ({} {}%) {:.4f}]".format(time_since(start), epoch,
                                                epoch/args.epochs*100,
                                                loss))
            print(generate(decoder, "Wh", 100, cuda=args.cuda), "\n")

    print("Saving...")
    save(decoder)

except KeyboardInterrupt:
    print("Saving before quitting...")
    save(decoder)

