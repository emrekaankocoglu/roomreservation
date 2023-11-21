from room.room import Room
from event.event import Event
from catalogue.catalogue import Catalogue
from query.query import Query
import datetime
class Organization:
    def __init__(self, name:str, rooms:[Room], events:[Event]):
        self.id = -1
        self.name = name
        self.rooms = rooms
        self.events = events
    
    @staticmethod
    def create(name:str, rooms:[Room], events:[Event]):
        organization = Organization(name, rooms, events)
        organization.id = Catalogue().registerOrganization(organization)
        return
    
    @staticmethod
    def get(id:int):
        return Catalogue().organizations[id]
    
    @staticmethod
    def retrieve(id:int):
        return Organization.get(id)
    
    @staticmethod
    def delete(id:int):
        del Catalogue().organizations[id]
        return
    
    @staticmethod
    def update(id:int, name:str, rooms:[Room], events:[Event]):
        organization = Organization(name, rooms, events)
        Catalogue().organizations[id] = organization
        return
    
    def reserve(self, event:Event, room:Room, start:datetime.datetime):
        event.assignPeriod(start, room)
        return
    def reassign(self, event:Event, room:Room, start:datetime.datetime):
        filter = {
            "event": event,
            "start": event.start,
            "end": event.start+event.duration,
            "rectangle": ((room.x, room.y), (0,0))
        }
        query = Query(filter, [room], self.events)
        if query.findRoom():
            event.assignPeriod(start, room)
            event.location = None
            event.start = None
        return

    def getRoom(self, id:int):
        return self.rooms[id]
    def updateRoom(self, id:int, room:Room):
        self.rooms[id] = room
        Catalogue().rooms[id].update(room)
        return
    def deleteRoom(self, id:int):
        del self.rooms[id]
        Catalogue().rooms[id].delete()
        return
    

