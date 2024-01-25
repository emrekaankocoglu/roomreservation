from tcp.packet import Packet
from tcp.reciever import TCPReciever, WSReciever
from argparse import ArgumentParser
from base64 import b64encode
import socket
from datetime import datetime, timedelta
from datetime import time
import websocket
import threading
# args should be username, password, host and port
parser = ArgumentParser()
parser.add_argument("username", help="Username")
parser.add_argument("password", help="Password")
parser.add_argument("host", help="Host")
parser.add_argument("port", help="Port")
args = parser.parse_args()
def on_open(ws):
    threading.Thread(target=user_input, args=(ws,)).start()
def on_receive(ws, message):
    print(message)
# Create socket
websocket.enableTrace(True)
host = f"ws://{args.host}:{args.port}"
s = websocket.WebSocketApp(host,
                           on_open=on_open,
                           on_message=on_receive)

def user_input(ws):
    while True:
        try:
            message = eval(input())
            packet = Packet("REQUEST", message, {"username":args.username, "password":args.password})
            Packet.send(s, packet)
        except Exception as e:
            print(e)
            continue



# Run the reciever thread
s.run_forever()

# read input from user, send it to server



