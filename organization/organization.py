from room.room import Room
from event.event import Event
from catalogue.catalogue import Catalogue
from catalogue.object import Object
from query.query import Query
import datetime
import os

class Organization(Object):
    def __init__(self, owner:int, name:str, map:str, rooms:dict, events:dict):
        self.id = -1
        self.owner = owner
        self.map = map
        self.name = name
        self.rooms = rooms
        self.events = events


    def registerRoom(self, room):
        room_dict = {
            room.id: room
        }
        self.rooms.update(room_dict)
        return room
    
    def registerEvent(self, event):
        event_dict = {
            event.id : event
        }
        self.events.update(event_dict)
        return event
    
    @staticmethod
    def create(owner:int, name:str, map:str, rooms:dict, events:dict):
        organization = Organization(owner, name, map, rooms, events)
        organization.id = Catalogue().registerOrganization(organization)
        return organization
    
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
    def update(id, **kwargs):
        org = Catalogue().organizations[id]
        for key, value in kwargs.items():
            if hasattr(org, key):
                setattr(org, key, value)
        return
    
    def reserve(self, event:Event, room:Room, start:datetime.datetime):
        if event.location is not None:
            raise Exception("Event already assigned")
        filter = {
            "event": event,
            "start": start,
            "end": start+event.duration,
            "rectangle": ((room.x, room.y), (0,0))
        }
        query = Query(filter, {room.id : room}, self.events)
        for x in query.findRoom():
            event.assignPeriod(start, room)
            return event
        raise Exception("Reservation failed: room not available")
    def reassign(self, event:Event, room:Room, start:datetime.datetime):
        filter = {
            "event": event,
            "start": start,
            "end": start+event.duration,
            "rectangle": ((room.x, room.y), (0,0))
        }
        query = Query(filter, {room.id: room}, self.events)
        for x in query.findRoom():
            event.assignPeriod(start, room)
            return event
        raise Exception("Reservation failed: room not available")
    def query(self, rectangle:((int,int),(int,int)), title:str, category:str, room:Room):
        filter = {
            "title": title,
            "category": category,
            "rectangle": rectangle,
            "room": room,
        }
        query = Query(filter, self.rooms, self.events)
        return query.queryIterator()
    def findRoom(self, event, rectangle:((int,int),(int,int)), start:datetime.datetime, end:datetime.datetime):
        filter = {
            "event": event,
            "start": start,
            "end": end,
            "rectangle": rectangle
        }
        query = Query(filter, self.rooms, self.events)
        return query.findRoom()
    def findSchedule(self, eventlist, rectangle:((int,int),(int,int)), start:datetime.datetime, end:datetime.datetime):
        filter = {
            "eventlist": eventlist,
            "start": start,
            "end": end,
            "rectangle": rectangle
        }
        query = Query(filter, self.rooms, self.events)
        return query.constructSchedule()
    
    def findScheduleInterval(self, eventlist, rectangle:((int,int),(int,int)), start:datetime.datetime, end:datetime.datetime, interval:datetime.timedelta):
        filter = {
            "eventlist": eventlist,
            "start": start,
            "end": end,
            "rectangle": rectangle,
            "interval": interval
        }
        query = Query(filter, self.rooms, self.events)
        return query.constructIntervalSchedule()

    def getRoom(self, id:int):
        return self.rooms[id]
    
    def updateRoom(self, id:int, updates:dict):
        room = self.rooms[id]
        room.update(**updates)
        return 
    
    def deleteRoom(self, id:int):
        del self.rooms[id]
        Room.delete(id)
        return
    

