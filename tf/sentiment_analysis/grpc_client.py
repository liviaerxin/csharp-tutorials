#!/usr/bin/env python3


"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function
import logging

import grpc


from .pbs import sentiment_analysis_pb2
from .pbs import sentiment_analysis_pb2_grpc


def run_say_hello():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = sentiment_analysis_pb2_grpc.SentimentAnalysisStub(channel)
        response = stub.SayHello(sentiment_analysis_pb2.HelloRequest(name='you'))
    print("Greeter client received: " + response.message)

def run_predict():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = sentiment_analysis_pb2_grpc.SentimentAnalysisStub(channel)
        response = stub.Predict(sentiment_analysis_pb2.PredictRequest(text='you are good'))
    print(f"Greeter client received: {response.positive}, {response.confidence}, {response.elapsed_time}")


"""test

python3 -m sentiment_analysis.grpc_client

"""

if __name__ == '__main__':
    logging.basicConfig()
    run_say_hello()
    run_predict()