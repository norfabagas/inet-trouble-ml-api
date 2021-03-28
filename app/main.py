from flask import Flask, request, jsonify, make_response
from werkzeug.wrappers import Request

app = Flask(__name__, instance_relative_config=False)

@app.route('/', methods=['GET'])
def home_view():
  information = {
    "name": "Internet trouble classification API",
    "author": "github.com/norfabagas",
    "version": "0.1"
  }

  return jsonify(information)