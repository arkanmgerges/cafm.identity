# https://www.youtube.com/watch?v=dQK0VLahrDk&list=PLXs6ze70rLY9u0X6qz_91bCvsjq3Kqn_O&index=5
"""The Python implememntation of seans grpc client"""
import os
import time
import grpc
import src.resource.proto._generated.pingpong_pb2 as pingpong_pb2
import src.resource.proto._generated.pingpong_pb2_grpc as pingpong_pb2_grpc
from src.resource.logging.logger import logger



def run():
    "The run method, that sends gRPC conformant messsages to the server"
    logger.info('coral.identity: Starting grpc client')
    counter = 0
    pid = os.getpid()
    with grpc.insecure_channel("server-grpc:9999") as channel:
        stub = pingpong_pb2_grpc.PingPongServiceStub(channel)
        while True:
            try:
                start = time.time()
                response = stub.ping(pingpong_pb2.Ping(count=counter))
                counter = response.count
                if counter % 1000 == 0:

                    # Compute item similarity matrix based on content attributes
                    logger.info(f'{time.time() - start}: resp= {response.count} : processId: {pid}')
                    # counter = 0
                time.sleep(0.001)
            except KeyboardInterrupt:
                print("KeyboardInterrupt")
                channel.unsubscribe(close)
                exit()


def close(channel):
    "Close the channel"
    channel.close()


if __name__ == "__main__":
    run()