from tcp.packet import Packet
from tcp.reciever import TCPReciever
from argparse import ArgumentParser
from base64 import b64encode
import socket
from datetime import datetime, timedelta
from datetime import time

# args should be username, password, host and port
parser = ArgumentParser()
parser.add_argument("username", help="Username")
parser.add_argument("password", help="Password")
parser.add_argument("host", help="Host")
parser.add_argument("port", help="Port")
args = parser.parse_args()

# Create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((args.host, int(args.port)))

# Run the reciever thread
reciever = TCPReciever(s, lambda packet: print(packet.message, packet.data, packet.auth))
reciever.start()

# read input from user, send it to server
while True:
    try:
        message = eval(input())
        packet = Packet("REQUEST", message, {"username":args.username, "password":args.password})
        Packet.send(s, packet)
    except KeyboardInterrupt:
        s.close()
        break


