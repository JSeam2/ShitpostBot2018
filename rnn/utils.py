import re
import pickle
import os
import unidecode
import string
import time
import math
import torch

# For strings
all_characters = string.printable
n_characters = len(all_characters)

# Regular expression to tokenize
punctuation_re = re.compile(r"([.,!?\"':;)(])")
digits_re = re.compile(r"\d")

# Special symbols
_PAD = "_PAD"
_GO = "_GO"
_EOS = "_EOS"
_UNK = "_UNK"
_START_VOCAB = [_PAD, _GO, _EOS, _UNK]

# Special tokenid
_PAD_ID = 0
_GO_ID = 1
_EOS_ID = 2
_UNK_ID = 3


def simple_tokenizer(sentence):
    """
    Converts a sentence into a list of tokens

    Args:
        sentence: String, some string we want to tokenize

    Returns:
        List of Strings, returns a list of string tokens
    """
    words = []
    for word in sentence.strip().split():
        words.extend(punctuation_re.split(word))

    return [x for x in words if x]


def create_vocab(max_vocab_size,
                 vocab_path="vocab.pkl",
                 data_path="data.pkl",
                 tokenizer=simple_tokenizer,
                 normalize_digits=False):
    """
    Create vocab from data file this is assumed to have come from preprocess.py

    Args:
        max_vocab_size: Int, limits the size of vocab
                        UNK token for words out of vocab
        vocab_path: String, path to save vocab
        data_path: String, path where data is saved, we expect a pkl file
        tokenizer: Function, function used to tokenize data. simple_tokenizer
                    used as default
        normalize_digits: Bool, when true sets all digits to 0
    """
    if os.path.isfile(vocab_path):
        print("Vocab file {} already exists. Delete or backup elsewhere"
              .format(vocab_path))
        return

    else:
        print("Creating vocab file at {}".format(vocab_path))
        print("Using data file at {}".format(data_path))

        vocab = {}

        with open(data_path, "rb") as f:
            data = pickle.load(f)
            counter = 0

            for line in data:
                counter += 1

                # for display
                if counter % 2000 == 0:
                    print("\tprocessing line {}".format(counter))

                tokens = tokenizer(line)

                for w in tokens:
                    if normalize_digits:
                        word = digits_re.sub("0", w)
                    else:
                        word = w

                    if word in vocab:
                        vocab[word] += 1
                    else:
                        vocab[word] = 1

            vocab_list = _START_VOCAB + sorted(vocab, key=vocab.get,
                                               reverse=True)

            # cull vocab list
            if len(vocab_list) > max_vocab_size:
                vocab_list = vocab_list[:max_vocab_size]

            pickle.dump(vocab_list, open(vocab_path, "wb"))


def init_vocab(vocab_path="./vocab.pkl"):
    """
    Initialize vocabulary from file

    We assume vocab is a python list
    we return a vocab in the form of {"A": 0, "B": 1} vocab to id
    and return a vocab in the form ["A", "B"] id to vocab.

    Args:
        vocab_path: path to pkl file containing the vocab list

    Returns:
        dict, dict: dict of string to int and reversed vocab which is a list
    """
    if not os.path.isfile(vocab_path):
        raise ValueError("Vocab file {} does not exist")

    else:
        with open(vocab_path, "rb") as f:
            vocab_list = pickle.load(f)
        vocab = dict([(x, y) for (y, x) in enumerate(vocab_list)])
        idtoword = dict([(y, x) for (y, x) in enumerate(vocab_list)])

        return vocab, idtoword


def sentence_to_token_id(sentence,
                         vocabulary,
                         tokenizer=simple_tokenizer,
                         normalize_digits=False):
    """
    Convert a string to a list of integer token id

    Turns
    Input sentence:
    ["This", "is", "a", "pear"]
    Input vocab:
    {"This": 1, "is": 4, "a": 5, "pear": 6}

    Into a string of integers mapping to the words
    [1, 4, 5, 6]

    Args:
        sentence: String, from data.pkl file to convert to tokenid
        vocabulary: Dictionary, maps tokens to integers
        tokenizer: Function, function used to tokenize, this is
            simple_tokenizer by default
        normalize_digits: Boolean, if true replace all digits with 0
            False by default

    Returns:
        List of Int, where the int are tokenid for the sentence
    """
    words = tokenizer(sentence)

    # mark with _UNK_ID if we do not recognize the words
    if normalize_digits:
        return [vocabulary.get(digits_re.sub("0", w), _UNK_ID) for w in words]
    else:
        return [vocabulary.get(w, _UNK_ID) for w in words]


def data_to_token_id(target_path="token_id.pkl",
                    data_path="data.pkl",
                    vocab_path="vocab.pkl",
                    tokenizer=simple_tokenizer,
                    normalize_digits=False):

    """
    Tokenize a data file into integer token id
    Calls sentence_to_token_id and saves the result to target_path

    Args:
        target_path: String, path to the place store tokenid
            "token_id.pkl" by default
        data_path: String, path to pkl file containing list of strings
            "data.pkl", by default
        vocab_path: String, path to pkl file containing vocab
            "vocab.pkl", by default
        tokenizer: Function, function used to tokenize, this is
            simple_tokenizer by default
        normalize_digits: Boolean, if true replace all digits with 0
            False by default
    """
    if os.path.isfile(target_path):
        print("Target file {} already exists. Delete or backup elsewhere"
              .format(target_path))
        return

    else:
        print("Tokenizing data and creating target file at {}"
              .format(target_path))
        print("Using data file at {}".format(data_path))
        print("Using vocab file at {}".format(vocab_path))

        # initialize vocab
        vocab, _ = init_vocab(vocab_path)

        with open(data_path, "rb") as datafile:
            with open(target_path, "wb") as tokenfile:
                data = pickle.load(datafile)

                token_ls = []
                counter = 0
                for line in data:
                    counter += 1
                    if counter % 1000 == 0:
                        print('\ttokenizing line {}'.format(counter))

                    token_ids = sentence_to_token_id(line, vocab, tokenizer,
                                                    normalize_digits)
                    token_ls.append(token_ids)

                pickle.dump(token_ls, tokenfile)


def read_file(filename):
    """
    Read file name

    Args:
        filename: String, path to file

    Returns:
        _file, len(file)
    """
    _file = unidecode.unidecode(open(filename).read())
    return _file, len(_file)


def char_tensor(string):
    """
    Turn a string into a character tensor used for character based learning

    Args:
        string: String, a string to convert to tensor

    Returns:
        tensor: pytorch tensor
    """
    tensor = torch.zeros(len(string)).long()

    for c in range(len(string)):
        try:
            tensor[c] = all_characters.index(string[c])

        except:
            continue

    return tensor


def time_since(since):
    """
    Time spent training

    Args:
        since: Int, initial time

    Return:
        String, time
    """
    s = time.time() - since
    m = math.floor(s/60)
    s -= m * 60
    return "{}m {}s".format(m, s)


if __name__ == "__main__":
    # create vocab file
    create_vocab(10000)

    # create token file
    data_to_token_id()
