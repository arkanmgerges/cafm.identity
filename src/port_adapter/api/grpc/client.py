# https://www.youtube.com/watch?v=dQK0VLahrDk&list=PLXs6ze70rLY9u0X6qz_91bCvsjq3Kqn_O&index=5
"""The Python implememntation of seans grpc client"""
import os
import time

import grpc
from grpc.beta.interfaces import StatusCode

from src.resource.logging.logger import logger
from src.resource.proto._generated.user_app_service_pb2 import UserAppService_userByNameAndPasswordRequest
from src.resource.proto._generated.user_app_service_pb2_grpc import UserAppServiceStub


def run():
    "The run method, that sends gRPC conformant messsages to the server"
    logger.info('coral.identity: Starting grpc client')
    counter = 0
    pid = os.getpid()
    with grpc.insecure_channel("localhost:9999") as channel:
        stub = UserAppServiceStub(channel)
        try:
            start = time.time()
            response = stub.userByNameAndPassword.with_call(
                UserAppService_userByNameAndPasswordRequest(name='arkan', password='12345'),
                metadata=(('auth_token', 'res-token-yumyum'),))
            # Compute item similarity matrix based on content attributes
            logger.info(f'{time.time() - start}: resp= {response} : processId: {pid}')
        except grpc.RpcError as e:
            # logger.info(e.status())
            logger.info(e.details())
            logger.info(e.code())
            logger.info(e.code() == StatusCode.NOT_FOUND)
            # logger.info(e)
        except Exception as e:
            logger.info(e)
        finally:
            channel.unsubscribe(close)
            exit(0)


def close(channel):
    "Close the channel"
    channel.close()


if __name__ == "__main__":
    run()