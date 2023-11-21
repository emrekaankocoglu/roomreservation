from room.room import Room
from event.event import event
class Organization:
    def __init__(self, name:str, rooms:[Room], events:[event]):
        self.id = -1
        self.name = name
        self.rooms = rooms
        self.events = events
    
    @staticmethod
    def create(name:str, rooms:[Room], events:[event]):
        organization = Organization(name, rooms, events)
        organization.id = Catalogue().registerOrganization(organization)
        return
    
    @staticmethod
    def get(id:int):
        return Catalogue().organizations[id]
    
    @staticmethod
    def retrieve(id:int):
        return get(id)
    
    @staticmethod
    def delete(id:int):
        del Catalogue().organizations[id]
        return
    
    @staticmethod
    def update(id:int, name:str, rooms:[Room], events:[event]):
        organization = Organization(name, rooms, events)
        Catalogue().organizations[id] = organization
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
    

