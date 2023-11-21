import datetime
from catalogue import Catalogue

class Room:
    def __init__(self, name:str, x, y, capacity:int, workinghours:(datetime.time, datetime.time), permissions:dict):
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
        return get(id)
    
    @staticmethod
    def delete(id:int):
        del Catalogue().rooms[id]
        return
    
    @staticmethod
    def update(id:int, name:str, x, y, capacity:int, workinghours:(datetime.time, datetime.time), permissions:dict):
        room = Room(name, x, y, capacity, workinghours, permissions)
        Catalogue().rooms[id] = room
        return room
    
