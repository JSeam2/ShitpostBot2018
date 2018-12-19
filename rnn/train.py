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
parser.add_argument('--data', type=str, default="data.pkl"
                    help='path to data')
parser.add_argument('--model', type=str, default='lstm',
                    help='Type of rnn (lstm, gru) lstm by default')
parser.add_argument('--emsize', type=int, default=1000,
                    help='Size of word embedding')
parser.add_argument('--nhidden', type=int, default=200,
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
parser.add_argument('--bptt', type=int, default=35,
                    help='sequence length')
parser.add_argument('--dropout', type=float, default=0.2,
                    help='Dropout applied to layers (0 = no dropout)')
parser.add_argument('--seed', type=int, default=1234,
                   help='random seed')
parser.add_argument('--cuda', action='store_true',
                   help='use CUDA')
parser.add_argument('--log-interval', type=int, default=200, metavar='N',
                    help='report interval')
parser.add_argument('--save', type=str, default='lstm.pt',
                   help='path to save the model')
parser.add_argument('--onnx-export', type=str, default='',
                    help='path to export the final model in onnx format')
args = parser.parse_args()

