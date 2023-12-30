import socket
from threading import Thread
from tcp.packet import Packet, HEADER_SIZE

class TCPReciever(Thread):
    def __init__(self, socket, callback):
        super().__init__()
        self.socket = socket
        self.callback = callback
    
    def run(self):
        while True:
            try:
                message = self.socket.recv(HEADER_SIZE)
                if message:
                    message_size = int(message.decode().strip())
                    while len(message) < message_size + HEADER_SIZE:
                        message += self.socket.recv(16)
                    packet = Packet.decode(message)
                self.callback(packet)
            except BrokenPipeError:
                print("Connection closed by client")
                self.socket.close()
                return
