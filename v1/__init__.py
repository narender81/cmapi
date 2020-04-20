from flask import Flask, jsonify, request
from enum import Enum

__version__ = "0.0.1"

class Status(Enum):
    READY = 1
    ACCEPTED = 2
    COLLECTED = 3
    DELIVERED = 4


app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello world'

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp





