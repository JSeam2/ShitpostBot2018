import random
import os

from flask import Blueprint, jsonify

from project.api.lstm import generate
from project.api.markov import markov

generator_blueprint = Blueprint("generator", __name__)


@generator_blueprint.route("/generator/ping", methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong'
    }), 200


@generator_blueprint.route("/generator/lstm", methods=['GET'])
def generate_lstm():
    # generate random seed
    val = random.randint(0, 9999)

    # sentence len
    sentence_len = 25

    # get current file path
    path = os.path.dirname(os.path.abspath(__file__))

    data_path = os.path.join(path, "lstm", "data.pkl")
    lstm_path = os.path.join(path, "lstm", "lstm.pt")

    # Generate text
    text = generate.generate_lstm(data_path=data_path,
                                  save_path=lstm_path,
                                  sentence_len=sentence_len,
                                  temperature=0.6,
                                  seed=val)

    return jsonify({
        'status': 'success',
        'message': text
    }), 200


@generator_blueprint.route("/generator/markov", methods=['GET'])
def generate_markov():
    # get current file path
    path = os.path.dirname(os.path.abspath(__file__))

    saved_model = os.path.join(path, "markov", "markov_model.json")

    # Generate text
    text = markov.generate_markov(saved_model=saved_model)

    return jsonify({
        'status': 'success',
        'message': text
    }), 200
