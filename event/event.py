from catalogue.catalogue import Catalogue
from room.room import Room
import datetime

class Event:
    def __init__(self, title:str, description:str, category:str, capacity:int, duration:datetime.timedelta, weekly:datetime.date, permissions:dict):
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
    def create(title:str, description:str, category:str, capacity:int, duration:datetime.timedelta, start:datetime.datetime, weekly:datetime.date, permissions:dict):
        event = Event(title, description, category, capacity, duration, start, weekly, permissions)
        event.id = Catalogue().registerEvent(event)
        return
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
    @staticmethod
    def update(id:int, title:str, description:str, category:str, capacity:int, duration:datetime.timedelta, start:datetime.datetime, weekly:datetime.date, permissions:dict):
        event = Event(title, description, category, capacity, duration, start, weekly, permissions)
        Catalogue().events[id] = event
        return
    def assignPeriod(self, start:datetime.datetime, location:Room):
        eventperms = self.permissions.get(Catalogue().getUser().id)
        if eventperms is None:
            raise Exception("User does not have permission to assign event")
        roomperms = Room.permissions.get(Catalogue().getUser().id)
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
            return (self.start, self.start+self.duration)
        else:
            start =+ datetime.timedelta(weeks=1)
            if start > self.weekly:
                return
            yield (start, start+self.duration)
        
        
    