#!/usr/bin/env python3

import json
import threading
import time
from multiprocessing import Process

from flask import Flask, jsonify, request
from flask_cors import CORS

from .sentiment_analysis import Model

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
cors = CORS(app)

model = Model()

@app.before_first_request  ## run before first request, not after the app starting up
def activate_job():
    print("aaa")
    # def run_job():
    #     while True:
    #         print("Run recurring task")
    #         time.sleep(3)

    # thread = threading.Thread(target=run_job)
    # thread.start()

@app.route("/")
def hello():
    return jsonify(message="Hello World!")

"""

http POST 0.0.0.0:5000/api/predict input="this film is really good"
"""

@app.route("/api/predict", methods=["POST"])
def predict():
    start = time.time()

    data = request.data.decode("utf-8")

    if data == "":
        params = request.form
        input = json.loads(params['text'])
    else:
        params = json.loads(data)
        input = params['text']

    input = str(input)

    ## TensorFlow
    positive, confidence = model.predict(input)

    ## END TensorFlow
    elapsed = time.time() - start
    return jsonify(positive=positive, confidence=confidence, elapsed_seconds=elapsed)

class WrapperServer(object):

    def __init__(self, app: Flask = app):
        super().__init__()
        self.app = app
        self.p: Process = None

    def start(self, *args, **kwargs):
        self.p = Process(target=app.run, args=args, kwargs=kwargs)
        self.p.start()        

    def stop(self):
        self.p.terminate()
        self.p.join()

"""test

python3 -m sentiment_analysis.flask_server

http POST 127.0.0.1:5000/api/predict text="this film is really good" 

"""
if __name__ == "__main__":
    print("start...")
    
    app.run(debug=None)
    
    # control the flask server run and stop
    # w = WrapperServer(app)
    # w.start()
    # time.sleep(20)
    # w.stop()
    # w.start()
    # time.sleep(10)
    # w.stop()
    print("end...")
