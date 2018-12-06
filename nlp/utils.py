import re
import pickle

# Regular expression to tokenize
punctuation_re = re.compile(b"([.,!?\"':;)(])")
digits_re = re.compile(br"\d")

def tokenizer(sentence):
    """
    Converts a sentence into a list of tokens
    """
    words = []
    for word in sentence.strip().split():
        words.extend(punctuation_re.split(word))

    return [x for x in words if x]


if __name__ == "__main__":
    
