import onoff_pb2
import onoff_pb2_grpc

import logging
import time

import grpc
import threading


def run(portnum):
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    logging.info(f'[{portnum}] Trying to connect')
    with grpc.insecure_channel(f'localhost:{portnum}') as channel:
        logging.info(f'[{portnum}] Connected to localhost')
        stub = onoff_pb2_grpc.onoffStub(channel)
        statestream = stub.GetStateStream(onoff_pb2.Empty())
        logging.info(f'[{portnum}] Got state stream')
        for state in statestream:
            logging.info(f'[{portnum}] Got state: {state.onoff}')
            if state.onoff == False:
                logging.info(f'[{portnum}] Set state to True')
                resp = stub.SetState(onoff_pb2.State(onoff=True))
                print(f'[{portnum}] Response {resp.success}')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    threads=[]
    for portnum in range(10000, 10100):
        logging.info(f'Main: Creating thread {portnum}')
        x = threading.Thread(target=run, args=(portnum,))
        logging.info(f'Main: Starting thread {portnum}')
        threads.append(x)
        x.start()
    threads[0].join()
