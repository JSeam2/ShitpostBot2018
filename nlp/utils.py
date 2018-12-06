import re
import pickle


# Regular expression to tokenize
punctuation_re = re.compile(r"([.,!?\"':;)(])")
digits_re = re.compile(r"\d")


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
                 vocab_path="./vocab.pkl",
                 data_path="./data.pkl",
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


if __name__ == "__main__":
    print(tokenizer("This is a some string."))
