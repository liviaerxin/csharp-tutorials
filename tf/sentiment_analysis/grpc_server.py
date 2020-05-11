#!/usr/bin/env python3

import logging
import time
from concurrent import futures

import grpc
from grpc_reflection.v1alpha import reflection

from .pbs import sentiment_analysis_pb2, sentiment_analysis_pb2_grpc

logger = logging.getLogger(__file__)

class SentimentAnalysis(sentiment_analysis_pb2_grpc.SentimentAnalysisServicer):
    from .sentiment_analysis import Model
    model = Model()

    def Predict(self, request, context):
        print('Predict...')
        start = time.time()
        input = str(request.text)

        ## TensorFlow
        positive, confidence = self.model.predict(input)

        ## END TensorFlow

        elapsed = time.time() - start

        return sentiment_analysis_pb2.PredictResponse(positive=positive, confidence=confidence, elapsed_time=elapsed)

    def SayHello(self, request, context):
        print('SayHello...')
        return sentiment_analysis_pb2.HelloReply(message='Hello, %s!' % request.name) 

def serve():
    logger.info('Starting...')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sentiment_analysis_pb2_grpc.add_SentimentAnalysisServicer_to_server(SentimentAnalysis(), server)
    SERVICE_NAMES = (
        sentiment_analysis_pb2.DESCRIPTOR.services_by_name['SentimentAnalysis'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

def creater_server():
    """
    server = creater_server()
    print("start...")
    server.start()
    time.sleep(20)
    print(f"stop...{server._state}")
    server.stop(True)

    # server = creater_server()
    # print(f"start...{server._state}")
    # server.start()
    # time.sleep(10)
    # print("stop...")
    # server.stop(True)
    """
    logger.info('Create gRPC Server...')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sentiment_analysis_pb2_grpc.add_SentimentAnalysisServicer_to_server(SentimentAnalysis(), server)
    SERVICE_NAMES = (
        sentiment_analysis_pb2.DESCRIPTOR.services_by_name['SentimentAnalysis'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    server.add_insecure_port('[::]:50051')
    return server


"""

python3 -m grpc_tools.protoc -I ../protos/ --python_out=./pbs --grpc_python_out=./pbs ../protos/sentiment_analysis.proto

grpcurl -plaintext localhost:50051 list

grpcurl -plaintext localhost:50051 list sentiment.analysis.SentimentAnalysis

grpcurl -plaintext localhost:50051 describe sentiment.analysis.SentimentAnalysis.Predict

grpcurl -plaintext -d '{"name": "you"} \
    localhost:50051 helloworld.Greeter/SayHello

grpcurl -plaintext -d '{"text": "m00"} \
    localhost:50051 sentiment.analysis.SentimentAnalysis/Predict
"""


"""test

python3 -m sentiment_analysis.grpc_server

"""

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    
    serve()

    # control server
    # server = creater_server()
    # print("start...")
    # server.start()
    # time.sleep(20)
    # print(f"stop...{server._state}")
    # server.stop(True)

    # server = creater_server()
    # print(f"start...{server._state}")
    # server.start()
    # time.sleep(10)
    # print("stop...")
    # server.stop(True)
