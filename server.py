from tcp.packet import Packet, WSPacket
from tcp.reciever import TCPReciever
from tcp.server.interface import TCPInterface, WSInterface
from argparse import ArgumentParser
from base64 import b64encode
import socket
from catalogue.object import Object
from main import main
from websockets.sync import server
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK
import threading
# args should be host and port
parser = ArgumentParser()
parser.add_argument("host", help="Host")
parser.add_argument("port", help="Port")
args = parser.parse_args()

# start listening to the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((args.host, int(args.port)+1))
s.listen()
# cat = main()
interfaces = []
cat = Object.load("Catalogue.pickle")

def tcpstart():
    while True:
        try:
            # accept a connection
            conn, addr = s.accept()
            print("Connection from", addr)

            # run the interface thread
            interface = TCPInterface(conn)
            interfaces.append(interface)

        except:
            for interface in interfaces:
                interface.close()
            s.close()
            cat.save()
            break

tcp = threading.Thread(target=tcpstart)
tcp.start()

    
def start(sock):
    print("Connection from", sock.remote_address)
    while True:
        try:
            message = sock.recv()
            print(message)
            packet = WSPacket.decode(message)
            interface = WSInterface(sock)
            interface.command_handler(packet)
        except ConnectionClosedOK:
            print("Connection closed by client")
            return
        except ConnectionClosedError:
            print("Connection closed by client")
            return
        

    

with server.serve(start, args.host, int(args.port)) as ws:
    ws.serve_forever()