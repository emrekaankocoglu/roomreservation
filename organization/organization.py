from room.room import Room
from event.event import Event
from catalogue.catalogue import Catalogue
from catalogue.object import Object
from query.query import Query
import datetime
import os

class Organization(Object):
    def __init__(self, owner:str, name:str, map:str, rooms:dict, events:dict, permissions:dict):
        Object.__init__(self)
        self.id = -1
        self.owner = owner
        self.map = map
        self.name = name
        self.rooms = rooms
        self.events = events
        self.permissions = permissions

    def check_permission(self, action:str, user:str, obj):
        if user == self.owner:
            return True
        if Catalogue().getUser(user).is_admin:
            return True
        if action in self.permissions.get(user):
            if action in ["deleteRoom", "deleteEvent", "updateRoom", "updateEvent"]:
                if obj.permissions.get(user) is not None and "WRITE" in obj.permissions.get(user):
                    return True
                else:
                    raise Exception("User does not have object level permission to perform action")
            else:
                return True
        raise Exception("User does not have permission to perform action")

    @Object.notify
    @Object.critical
    def registerRoom(self, room):
        room_dict = {
            room.id: room
        }
        self.rooms.update(room_dict)
        return room
    
    @Object.notify
    @Object.critical
    def registerEvent(self, event):
        event_dict = {
            event.id : event
        }
        self.events.update(event_dict)
        return event
    
    @staticmethod
    def create(owner:int, name:str, map:str, rooms:dict, events:dict, permissions:dict):
        organization = Organization(owner, name, map, rooms, events, permissions)
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
    
    @Object.notify
    @Object.critical
    def reserve(self, event:Event, room:Room, start:datetime.datetime, username:str):
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
            event.assignPeriod(start, room, username)
            return event
        raise Exception("Reservation failed: room not available")
    
    @Object.notify
    @Object.critical
    def reassign(self, event:Event, room:Room, start:datetime.datetime, username:str):
        filter = {
            "event": event,
            "start": start,
            "end": start+event.duration,
            "rectangle": ((room.x, room.y), (0,0))
        }
        query = Query(filter, {room.id: room}, self.events)
        for x in query.findRoom():
            event.assignPeriod(start, room, username)
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
    
    @Object.notify
    @Object.critical
    def updateRoom(self, id:int, updates:dict):
        room = self.rooms[id]
        room.update(**updates)
        return 
    
    @Object.notify
    @Object.critical
    def deleteRoom(self, id:int):
        del self.rooms[id]
        Room.delete(id)
        return
    
    def createRoom(self, name:str, x:int, y:int, capacity:int, workinghours:(datetime.time, datetime.time), permissions:dict):
        room = Room.create(name, x, y, capacity, workinghours, permissions)
        self.registerRoom(room)
        return room
    
    def getEvent(self, id:int):
        return self.events[id]
    
    @Object.notify
    @Object.critical
    def updateEvent(self, id:int, updates:dict):
        event = self.events[id]
        event.update(**updates)
        return
    
    @Object.notify
    @Object.critical
    def deleteEvent(self, id:int):
        del self.events[id]
        Event.delete(id)
        return
    
    def createEvent(self, title:str, description:str, category:str, capacity:int, duration:datetime.timedelta, weekly:datetime.datetime, permissions:dict):
        event = Event.create(title, description, category, capacity, duration, weekly, permissions)
        self.registerEvent(event)
        return event
    

