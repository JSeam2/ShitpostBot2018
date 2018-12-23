import pickle
import markovify
import json

# convert pkl file into txt file


def build_text_model(data_path="data.pkl"):
    """
    Build text model

    Args:
        data_path: String, file path of extracted data, default="data.pkl"
    """
    with open("data.pkl", "rb") as f:
        data = pickle.load(f)

    text_model = markovify.Text(data)

    with open("markov_model.json", "w") as f:
        f.write(text_model.to_json())

    return text_model


def generate_text_model(saved_model="markov_model.json"):
    with open(saved_model, 'r') as f:
        data = f.read()
        text_model = markovify.Text.from_json(data)
    gen = text_model.make_short_sentence(150)

    return gen


if __name__ == "__main__":
    build_text_model()
    print(generate_text_model())
