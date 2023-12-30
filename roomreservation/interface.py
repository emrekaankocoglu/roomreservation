import socket
from tcp.packet import Packet, HEADER_SIZE

from django.http import Http404

class TCPInterfaceInstance:
    def __init__(self):
        pass

    def __enter__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(("localhost", 5000))
        return self
    def __exit__(self, type, value, traceback):
        self.socket.close()

    def send(self, packet):
        Packet.send(self.socket, packet)
    
    def receive(self):
        try:
            message = self.socket.recv(HEADER_SIZE)
            if message:
                message_size = int(message.decode().strip())
                while len(message) < message_size + HEADER_SIZE:
                    message += self.socket.recv(16)
                packet = Packet.decode(message)
                return packet
        except BrokenPipeError:
            print("Connection closed by client")
            self.socket.close()
            raise Http404("Connection closed by client")
    
    def close(self):
        self.socket.close()


