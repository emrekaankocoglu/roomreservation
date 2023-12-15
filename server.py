from tcp.packet import Packet
from tcp.reciever import TCPReciever
from tcp.server.interface import TCPInterface
from argparse import ArgumentParser
from base64 import b64encode
import socket
from catalogue.object import Object
from main import main

# args should be host and port
parser = ArgumentParser()
parser.add_argument("host", help="Host")
parser.add_argument("port", help="Port")
args = parser.parse_args()

# start listening to the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((args.host, int(args.port)))
s.listen()
# cat = main()
interfaces = []
cat = Object.load("Catalogue.pickle")

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

    
