"""
Adapted from pytorch/examples/word_language_model
"""

import argparse
import time
import math
import os
import torch
import torch.nn as nn
import torch.onnx

import data
import model_rnn

parser = argparse.ArgumentParser(description="Shitpost Bot LSTM")
parser.add_argument('--data', type=str, default="data.pkl",
                    help='path to data')
parser.add_argument('--model', type=str, default='lstm',
                    help='Type of rnn (lstm, gru) lstm by default')
parser.add_argument('--emsize', type=int, default=300,
                    help='Size of word embedding')
parser.add_argument('--nhidden', type=int, default=300,
                    help='Number of hidden units per layer')
parser.add_argument('--nlayers', type=int, default=2,
                    help='Number of layers')
parser.add_argument('--lr', type=float, default=20,
                    help='Initial learning rate')
parser.add_argument('--clip', type=float, default=0.25,
                    help='Gradient clipping to prevent exploding gradients')
parser.add_argument('--epochs', type=int, default=40,
                    help='upper epoch limit')
parser.add_argument('--batch_size', type=int, default=20, metavar='N',
                    help='batch size')
parser.add_argument('--bptt', type=int, default=25,
                    help='sequence length')
parser.add_argument('--dropout', type=float, default=0.5,
                    help='Dropout applied to layers (0 = no dropout)')
parser.add_argument('--seed', type=int, default=1234,
                    help='random seed')
parser.add_argument('--cuda', action='store_true',
                    help='use CUDA')
parser.add_argument('--log-interval', type=int, default=20, metavar='N',
                    help='report interval')
parser.add_argument('--save', type=str, default='lstm.pt',
                    help='path to save the model')
parser.add_argument('--onnx-export', type=str, default='',
                    help='path to export the final model in onnx format')
args = parser.parse_args()

# Set random seed to ensure we can reproduce results in case of debugging
torch.manual_seed(args.seed)

# Check for cuda
if torch.cuda.is_available():
    if not args.cuda:
        print("WARNING: You have a CUDA device, "
              "you should probably run with --cuda")

device = torch.device("cuda" if args.cuda else "cpu")


#################
# LOAD DATA
#################

corpus = data.Corpus(args.data)


def batchify(data, batch_size):
    """
    Divide the data into batch size

    From sequential data, batchify arranges the dataset into columns

    Example:
        a g m s
        b h n t
        c i o u
        d j p v
        e k q w
        f l r x

        Each of the column is treated independently. This means that
        the depednece of e. g. "g" on "f" cannot be learned, but allows
        for more efficient batch processing

    Args:
        data: List of Tensors, this  are ids obtained after tokenization
        batch_size: Int, size of the batch

    Return:
        batched ids, list of tensors
    """
    # Split the data into
    num_batch = data.size(0) // batch_size

    # Trim off excess elements that do not fit
    data = data.narrow(0, 0, num_batch * batch_size)

    # Evenly divide data across batches
    data = data.view(batch_size, -1).t().contiguous()

    return data.to(device)


eval_batch_size = args.batch_size
train_data = batchify(corpus.train, args.batch_size)
val_data = batchify(corpus.valid, args.batch_size)
test_data = batchify(corpus.test, args.batch_size)


#################
# BUILD MODEL
#################

num_tokens = len(corpus.dictionary)

if args.model.lower() == 'lstm':
    model = model_rnn.LSTMModel(num_tokens, args.emsize, args.nhidden,
                                args.nlayers, args.dropout).to(device)

elif args.model.lower() == 'gru':
    model = model_rnn.GRUModel(num_tokens, args.emsize, args.nhidden,
                               args.nlayers, args.dropout).to(device)

else:
    raise ValueError('{} in --model argument is not'
                     'recognized'.format(args.model))

criterion = nn.CrossEntropyLoss()


#################
# BUILD MODEL
#################

def repackage_hidden(h):
    """
    Wraps the hidden state in new Tensors, to detach them from their history
    """
    if isinstance(h, torch.Tensor):
        return h.detach()
    else:
        return tuple(repackage_hidden(v) for v in h)


def get_batch(source, i):
    """
    get_batch subdivides the source data in chunks of length args.bptt
    If source is equal to the example output of the batchify function,
    with a bptt-limit of 2, we'd get the following two Variables for
    i = 0:
        a g m s     b h n t
        b h n t     c i o u

    Note that despite the name of the function, the subdivision of data is
    not done along the batch dimension (ie. dimension 1), since that was
    handled by the batchify function. The chunks are along dimension 0,
    corresponding to the seq_len dimension in the LSTM

    Args:
        source: data after the batchify function is used
        i: Int, some index

    Returns:
        data: section from source
        target: another section from the source
    """
    seq_len = min(args.bptt, len(source) - 1 - i)
    data = source[i:i+seq_len]
    target = source[i + 1: i + 1 + seq_len].view(-1)
    return data, target


def evaluate(data_source):
    """
    Evaluate the data source
    """
    model.eval()
    total_loss = 0.
    num_tokens = len(corpus.dictionary)
    hidden = model.init_hidden(eval_batch_size)
    with torch.no_grad():
        for i in range(0, data_source.size(0) - 1, args.bptt):
            data, targets = get_batch(data_source, i)
            output, hidden = model(data, hidden)
            output_flat = output.view(-1, num_tokens)
            total_loss += len(data) * criterion(output_flat, targets).item()
            hidden = repackage_hidden(hidden)

    return total_loss / (len(data_source) - 1)


def train():
    model.train()
    total_loss = 0.
    start_time = time.time()
    num_tokens = len(corpus.dictionary)
    print("TAKE NOTE: NUM TOKENS USED: {}".format(num_tokens))
    hidden = model.init_hidden(args.batch_size)

    for batch, i in enumerate(range(0, train_data.size(0) - 1, args.bptt)):
        data, targets = get_batch(train_data, i)

        # detach hidden state from how it was produced
        # otherwise the model will backprop till the start of the
        # dataset
        hidden = repackage_hidden(hidden)
        model.zero_grad()
        output, hidden = model(data, hidden)
        loss = criterion(output.view(-1, num_tokens), targets)
        loss.backward()

        # perform clipping to prevent exploding gradients
        torch.nn.utils.clip_grad_norm_(model.parameters(), args.clip)

        for p in model.parameters():
            p.data.add_(-lr, p.grad.data)

        total_loss += loss.item()

        if batch % args.log_interval == 0 and batch > 0:
            cur_loss = total_loss / args.log_interval
            elapsed = time.time() - start_time
            print('| epoch {:3d} | {:5d}/{:5d} batches | lr {:02.2f} | '
                  'ms/batch{:5.2f} | loss {:5.2f} | ppl {:8.2f}'.format(
                      epoch, batch, len(train_data) // args.bptt, lr,
                      elapsed * 1000 / args.log_interval, cur_loss,
                      math.exp(cur_loss)))

            total_loss = 0
            start_time = time.time()


def export_onnx(path, batch_size, seq_len):
    print('The model is also exported in ONNX format at {}'.
          format(os.path.realpath(args.onnx.export)))
    model.eval()
    dummy_input = torch.LongTensor(seq_len * batch_size).zero_(
                    ).view(-1, batch_size).to(device)

    hidden = model.init_hidden(batch_size)
    torch.onnx.export(model, (dummy_input, hidden), path)


lr = args.lr
best_val_loss = None


# Allow for ctrl + c to break out of training
try:
    print('-' * 89)
    print("START TRAINING")
    print('-' * 89)

    for epoch in range(1, args.epochs+1):
        epoch_start_time = time.time()
        train()
        val_loss = evaluate(val_data)
        print('-' * 89)
        print('| end of epoch {:3d} | time: {:5.2f}s | valid loss {:5.2f} | '
              'valid ppl {:8.2f}'.format(epoch,
                                         (time.time() - epoch_start_time),
                                         val_loss,
                                         math.exp(val_loss)))

        print('-' * 89)

        # Save the model if the validation loss is the best we've seen so far
        if not best_val_loss or val_loss < best_val_loss:
            with open(args.save, 'wb') as f:
                torch.save(model.state_dict(), f)
            best_val_loss = val_loss

        else:
            # Anneal learning rate if no improvement has been seen
            lr /= 4.0

except KeyboardInterrupt:
    print('-' * 89)
    print('Exiting from training early')


# Run on test data
test_loss = evaluate(test_data)
print('=' * 89)
print('| End of training | test loss {:5.2f} | test ppl {:8.2f}'.format(
    test_loss, math.exp(test_loss)))
print('=' * 89)

if len(args.onnx_export) > 0:
    # Export the model in ONNX format
    export_onnx(args.onnx_export, batch_size=1, seq_len=args.bptt)
