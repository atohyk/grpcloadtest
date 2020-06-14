import onoff_pb2
import onoff_pb2_grpc
import random
import concurrent.futures as futures
import logging
import grpc
import time
import threading

class onoffServicer(onoff_pb2_grpc.onoffServicer):
    def __init__(self):
        self.state = False
        print(f'Created state {self.state}')

    def GetStateStream(self, request, context):
        print(f'State: {self.state}')
        while True:
            print(f'Yielding {self.state}')
            yield onoff_pb2.State(onoff=self.state)
            time.sleep(2)
            if random.random() > 0.9 and self.state:
                self.state = False
                print('Switching state to False')

    def SetState(self, request, context):
        if request.onoff:
            if random.random()>0.2:
                self.state = True
                return onoff_pb2.RequestStatus(success=True)
        return onoff_pb2.RequestStatus(success=False)

def serve(portnum):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    onoff_pb2_grpc.add_onoffServicer_to_server(
        onoffServicer(), server)
    server.add_insecure_port(f'[::]:{portnum}')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    threads=[]
    for portnum in range(10000, 10100):
        logging.info(f'Main: Creating server thread {portnum}')
        x = threading.Thread(target=serve, args=(portnum,))
        logging.info(f'Main: Starting server thread {portnum}')
        threads.append(x)
        x.start()
    threads[0].join()
