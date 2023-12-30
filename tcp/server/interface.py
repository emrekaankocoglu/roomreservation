from tcp.packet import Packet
from tcp.reciever import TCPReciever
from tcp.notifier import TCPNotifier
from catalogue.catalogue import Catalogue
from event.event import Event
from room.room import Room
from user.user import User
from organization.organization import Organization
from view.view import View
from threading import Thread
import traceback





class TCPInterface:
    def __init__(self, socket):
        self.socket = socket
        self.reciever = TCPReciever(self.socket, self.command_handler)
        self.reciever.start()
        self.notifiers = []
    def command_handler(self, packet):
        try:
            if packet.auth.get("password"):
                user = User.login(packet.auth["username"], packet.auth["password"])
            elif packet.auth["token"]:
                user = User.loginWithToken(packet.auth["username"], packet.auth["token"])
            print(f"User {user.username} logged in")

            organization = Catalogue().getid(packet.data["organization"]) if "organization" in packet.data else None


            if packet.data["command"] == "listObject":
                if user.is_admin:
                    obj = Catalogue().listobject()
                else:    
                    raise Exception("Not authorized")
                
            elif packet.data["command"] == "listRoom":
                organization.check_permission(packet.data["command"], user.username, None)
                obj = organization.rooms
            elif packet.data["command"] == "createRoom":
                organization.check_permission(packet.data["command"], user.username, None)
                obj = organization.createRoom(**packet.data["room"])
            elif packet.data["command"] == "updateRoom":
                organization.check_permission(packet.data["command"], user.username, organization.getRoom(packet.data["room"]["id"]))
                obj = organization.updateRoom(packet.data["room"]["id"],packet.data["room"])
            elif packet.data["command"] == "deleteRoom":
                organization.check_permission(packet.data["command"], user.username, organization.getRoom(packet.data["room"]["id"]))
                obj = organization.deleteRoom(packet.data["room"]["id"])

            elif packet.data["command"] == "listEvent":
                organization.check_permission(packet.data["command"], user.username, None)
                obj = organization.events
            elif packet.data["command"] == "createEvent":
                organization.check_permission(packet.data["command"], user.username, None)
                obj = organization.createEvent(**packet.data["event"])
            elif packet.data["command"] == "updateEvent":
                organization.check_permission(packet.data["command"], user.username, organization.getEvent(packet.data["event"]["id"]))
                obj = organization.updateEvent(packet.data["event"]["id"],packet.data["event"])
            elif packet.data["command"] == "deleteEvent":
                organization.check_permission(packet.data["command"], user.username, organization.getEvent(packet.data["event"]["id"]))
                obj = organization.deleteEvent(packet.data["event"]["id"])
            
            elif packet.data["command"] == "reserve":
                organization.check_permission(packet.data["command"], user.username, None)
                event = organization.getEvent(packet.data["event"]["id"])
                room = organization.getRoom(packet.data["room"]["id"])
                obj = organization.reserve(event, room, packet.data["start"], user.username)
            
            elif packet.data["command"] == "findSchedule":
                eventlist = [organization.getEvent(id) for id in packet.data["eventlist"]]
                obj = organization.findSchedule(eventlist, packet.data["rectangle"], packet.data["start"], packet.data["end"])
            elif packet.data["command"] == "findScheduleInterval":
                eventlist = [organization.getEvent(id) for id in packet.data["eventlist"]]
                obj = organization.findScheduleInterval(eventlist, packet.data["rectangle"], packet.data["start"], packet.data["end"], packet.data["interval"])

            elif packet.data["command"] == "addQuery":
                obj = user.view.addquery(organization.id, **packet.data["query"])
            elif packet.data["command"] == "delQuery":
                obj = user.view.delquery(packet.data["query"]["id"])
            elif packet.data["command"] == "listQuery":
                obj = user.view.queryset

            elif packet.data["command"] == "roomView":
                obj = user.view.roomView(packet.data["start"], packet.data["end"])
                thread = TCPNotifier(self.socket, user=user, view_type="roomView", start_time=packet.data["start"], end_time=packet.data["end"], view_result=str(obj))
                thread.start()
                self.notifiers.append(thread)
            elif packet.data["command"] == "dayView":
                obj = user.view.dayView(packet.data["start"], packet.data["end"])
                thread = TCPNotifier(self.socket, user=user, view_type="dayView", start_time=packet.data["start"], end_time=packet.data["end"], view_result=str(obj))
                thread.start()
                self.notifiers.append(thread)
            
            elif packet.data["command"] == "attach":
                obj = Catalogue().getid(packet.data["id"])
                thread = TCPNotifier(self.socket, item=obj)
                thread.start()
                self.notifiers.append(thread)

            elif packet.data["command"] == "detach":
                obj = Catalogue().getid(packet.data["id"])
                for thread in self.notifiers:
                    if thread.item == obj:
                        thread.item = None
                        break
            else:
                raise Exception("Command not found")

            response = Packet("OK", {"command": packet.data["command"], "response": obj}, packet.auth)
            Packet.send(self.socket, response)
        except Exception as e:
            # send error message
            response = Packet("ERROR", {"command": packet.data["command"], "response": str(e)}, packet.auth)
            Packet.send(self.socket, response)
            traceback.print_exc()
        print("response sent")
        return
    
    def close(self):
        for thread in self.notifiers:
            thread.item = None
            thread.view_type = None
        self.socket.close()

        print("Interface closed")


        


        


