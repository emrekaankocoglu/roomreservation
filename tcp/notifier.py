from threading import Thread
from tcp.packet import Packet, WSPacket, serialize
from catalogue.catalogue import Catalogue
import json
import datetime

class TCPNotifier(Thread):
    def __init__(self, socket, user=None, item=None, view_type=None, start_time=None, end_time=None, view_result=""):
        super().__init__()
        self.socket = socket
        self.user = user
        self.item = item
        self.view_type = view_type
        self.start_time = start_time
        self.end_time = end_time
        self.view_result = view_result


    def run(self):
        while True:
            if self.item is not None:
                with self.item.updated:
                    self.item.updated.wait()
                if self.item is not None:
                    packet = Packet("NOTIFY", {"command": "attach", "response": self.item})
                    Packet.send(self.socket, packet)
            elif self.view_type is not None:
                view = self.user.view
                if view.queryset:
                    if view is not None and view.queryset:
                        for k,v in view.queryset.items():
                            with Catalogue().getid(v[1]).updated:
                                Catalogue().getid(v[1]).updated.wait()
                            self.checkupdate()
            else:
                print("Detached notifier")
                return
    
    def checkupdate(self):
        print("Checking update")
        if self.view_type == "roomView":
            result = str(self.user.view.roomView(self.start_time, self.end_time))
        elif self.view_type == "dayView":
            result = str(self.user.view.dayView(self.start_time, self.end_time))
        if result != self.view_result:
            self.view_result = result
            packet = Packet("NOTIFY", {"command": self.view_type, "response": result}, self.user.username)
            Packet.send(self.socket, packet)

class WSNotifier(Thread):
    def __init__(self, socket, user=None, item=None, view_type=None, start_time=None, end_time=None, view_result=""):
        super().__init__()
        self.socket = socket
        self.user = user
        self.item = item
        self.view_type = view_type
        self.start_time = start_time
        self.end_time = end_time
        self.view_result = view_result


    def run(self):
        while True:
            if self.item is not None:
                with self.item.updated:
                    self.item.updated.wait()
                if self.item is not None:
                    packet = WSPacket("NOTIFY", {"command": "attach", "response": self.item})
                    WSPacket.send(self.socket, packet)
            elif self.view_type is not None:
                view = self.user.view
                if view.queryset:
                    if view is not None and view.queryset:
                        for k,v in view.queryset.items():
                            with Catalogue().getid(v[1]).updated:
                                Catalogue().getid(v[1]).updated.wait()
                            self.checkupdate()
            else:
                print("Detached notifier")
                return
    
    def checkupdate(self):
        print("Checking update")
        if self.view_type == "roomView":
            obj = self.user.view.roomView(self.start_time, self.end_time)
            for k,v in obj.items():
                if isinstance(k, datetime.datetime):
                    k = k.isoformat()
            result = json.dumps(obj, default=serialize,
                                sort_keys=True)
        elif self.view_type == "dayView":
            obj = self.user.view.dayView(self.start_time, self.end_time)
            n = {}
            for k,v in obj.items():
                if isinstance(k, datetime.date):
                    n[k.isoformat()] = v
            obj = n
            result = json.dumps(obj, default=serialize,
                                sort_keys=True)
        if result != self.view_result:
            self.view_result = result
            result = json.loads(result)
            packet = WSPacket("NOTIFY", {"command": self.view_type, "response": result}, self.user.username)
            WSPacket.send(self.socket, packet)