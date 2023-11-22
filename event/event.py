from catalogue.catalogue import Catalogue
from catalogue.object import Object
from room.room import Room
import datetime

class Event(Object):
    def __init__(self, title:str, description:str, category:str, capacity:int, duration:datetime.timedelta, weekly:datetime.datetime, permissions:dict):
        self.id = -1
        self.title = title
        self.description = description
        self.category = category
        self.capacity = capacity
        self.duration = duration
        self.start = None
        self.weekly = weekly
        self.permissions = permissions
        self.location = None
    
    @staticmethod
    def create(title:str, description:str, category:str, capacity:int, duration:datetime.timedelta, weekly:datetime.datetime, permissions:dict):
        event = Event(title, description, category, capacity, duration, weekly, permissions)
        event.id = Catalogue().registerEvent(event)
        return event
    @staticmethod
    def get(id:int):
        return Catalogue().events[id]
    @staticmethod
    def retrieve(id:int):
        return Event.get(id)
    @staticmethod
    def delete(id:int):
        del Catalogue().events[id]
        return
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self
    
    def assignPeriod(self, start:datetime.datetime, location:Room):
        eventperms = self.permissions.get(Catalogue().getUser().id)
        if eventperms is None:
            raise Exception("User does not have permission to assign event")
        roomperms = location.permissions.get(Catalogue().getUser().id)
        if roomperms is None:
            raise Exception("User does not have permission to assign room")
        if self.weekly and "PERWRITE" not in roomperms:
            raise Exception("User does not have permission to assign weekly event for room")
        elif "WRITE" not in roomperms:
            raise Exception("User does not have permission to assign event for room")
        
        
        self.start = start
        self.location = location.id
        return
    def getTimePeriod(self):
        start = self.start
        if self.weekly is None:
            yield (self.start, self.start+self.duration)
        else:
            while start < self.weekly:
                yield (start, start+self.duration)
                start = start + datetime.timedelta(weeks=1)
        return

    
                
            
        
        
    