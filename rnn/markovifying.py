import cPickle as pickle
import numpy as np
import pandas as pandas
import spacy
import random
import re

data = pickle.load(open("data.pkl", "rb"))
output = open("output.txt", "w")
output.write(str(data))
output.flush()
output.close()

output.headline_text[random.sample(range(100),10)]

def build_text_model():
     text_model0 = markovify.Text(output.headline_text, state_size = 2, chain = None)
     text_model1 = markovify.Text(output.headline_text, state_size = 3, chain = None)
     text_model2 = markovify.Text(output.headline_text, state_size = 4, chain = None)
     model_combined = markovify.combine([text_model0, text_model1, text_model2], [1.5, 1, 1])
     return model_combined

def generate_text_model(model_combined, number=40, short=False):
     count = 0
     while count < number:
          if short:
               model = model_combined.make_short_sentence(140)
          else:
               model = model_combined.make_sentence()

          if model:
               count +=1
               print("Model {}".format(count))
               print(model)
               print()


if __name__ == "__main__":
     text_model = generate_text_model(build_text_model())