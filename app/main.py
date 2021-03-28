from flask import Flask, request, jsonify, make_response
from werkzeug.wrappers import Request
import numpy as np
from keras.models import load_model
from keras.preprocessing.text import tokenizer_from_json
from keras.preprocessing import sequence
import re
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import json
import os


app = Flask(__name__, instance_relative_config=False)

@app.route('/', methods=['GET'])
def home_view():
  information = {
    "name": "Internet trouble classification API",
    "author": "github.com/norfabagas",
    "version": "0.1"
  }

  return jsonify(information)

@app.route('/classify', methods=['GET'])
def classify_view():
  # Output categories
  text_categories = ['INTERNET', 'IPTV', 'VOICE', 'NN']

  # load saved keras model
  model_dir = "saved_model/keras/model.h5"
  model = load_model(os.path.abspath(model_dir))

  # load saved tokenizer
  tokenizer_dir = "saved_model/tokenizer/tokenizer.json"
  with open(os.path.abspath(tokenizer_dir)) as f:
    data = json.load(f)
    tokenizer = tokenizer_from_json(data)
  
  # retrieve text
  text = request.args.get('text', default='undefined', type=str)
  
  # set it as numpy
  text_in_array = [text]
  text_in_array = np.array(text_in_array)

  # Initialize stopwords
  factory = StopWordRemoverFactory()
  stopwords = factory.create_stop_word_remover()

  # Remove punctuation
  punctuated_text = [re.sub(r'[^\w\s]', '', text) for text in text_in_array]

  # Lowerize it and apply stopwords
  lowerized_text = [stopwords.remove(text.lower()) for text in punctuated_text]

  # Tokenize it
  tokenized_text = tokenizer.texts_to_sequences(lowerized_text)

  # Pad the sequence to the same length
  max_padded = 20
  padded_text = sequence.pad_sequences(tokenized_text, maxlen=max_padded)

  # Pad the numpy into 1D array
  z = padded_text[0].reshape(1, 20)

  # Predict it
  result = model.predict(z)

  arr = result.tolist()
  index = arr[0].index(max(arr[0]))
  print(text_categories[index])

  
  return jsonify(
    {
      "prediction": text_categories[index],
      "result": {
        text_categories[0]: arr[0][0],
        text_categories[1]: arr[0][1],
        text_categories[2]: arr[0][2],
        text_categories[3]: arr[0][3],
      },
      "text": {
        "default": text,
        "factory_punctuated": punctuated_text,
        "stopwords_lowerized": lowerized_text,
        "tokenized": tokenized_text,
        "tokenized_padded": padded_text.tolist()
      },
      "tokenizer": tokenizer.to_json()
    }
  )
