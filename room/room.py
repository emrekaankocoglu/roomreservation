import datetime
from catalogue.catalogue import Catalogue
from catalogue.object import Object

class Room(Object):
    def __init__(self, name:str, x, y, capacity:int, workinghours:(datetime.time, datetime.time), permissions:dict):
        super().__init__()
        self.id = -1
        self.name = name
        self.x = x
        self.y = y
        self.capacity = capacity
        self.workinghours = workinghours
        self.permissions = permissions
    
    @staticmethod
    def create(name:str, x, y, capacity:int, workinghours:(datetime.time, datetime.time), permissions:dict):
        room = Room(name, x, y, capacity, workinghours, permissions)
        room.id = Catalogue().registerRoom(room)
        return room
    
    @staticmethod
    def get(id:int):
        return Catalogue().rooms[id]
    
    @staticmethod
    def retrieve(id:int):
        return Room.get(id)
    
    @staticmethod
    def delete(id:int):
        del Catalogue().rooms[id]
        for id, event in Catalogue().events.items():
            if event.location == id:
                event.location = None
                event.start = None
        return
    
    @Object.critical
    @Object.notify
    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

        return self
    
    
