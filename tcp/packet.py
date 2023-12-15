import pickle

HEADER_SIZE = 10

class Packet:
    def __init__(self, message = "", data:dict = {}, auth = None):
        self.message = message
        self.data = data
        self.auth = auth
    
    def encode(self):
        payload = {"message": self.message,
                   "data" :  self.data,
                   "auth" : self.auth}
        pickled_payload = pickle.dumps(payload)
        payload_size = len(pickled_payload)
        packet_message = f"{payload_size:<{HEADER_SIZE}}".encode() + pickled_payload
        return packet_message
    
    @staticmethod
    def decode(packet):
        packet_payload = packet[HEADER_SIZE:]
        payload = pickle.loads(packet_payload)
        packet = Packet(payload["message"], payload["data"], payload["auth"])
        return packet
    
    @staticmethod
    def send(socket, packet):
        socket.send(packet.encode())
