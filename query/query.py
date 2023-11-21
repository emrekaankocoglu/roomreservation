from room.room import Room
from event.event import Event
import datetime

class Query:
    def __init__(self, filter:dict, rooms:[Room], events:[Event]):
        self.filter = filter
        self.rooms = rooms
        self.events = events

    
    @staticmethod
    def in_rectangle(x:int, y:int, rectangle:((int, int), (int, int))):
        return x >= rectangle[0][0] and x <= rectangle[0][0]+rectangle[1][0] and y >= rectangle[0][1] and y <= rectangle[0][1]+rectangle[1][1]
    @staticmethod
    def collide(interval1: (datetime.datetime, datetime.datetime), interval2: (datetime.datetime, datetime.datetime)):
        return interval1[0] <= interval2[1] and interval1[1] >= interval2[0]
     
    def findRoom(self):
        for room in self.rooms:
            if not Query.in_rectangle(room.x, room.y, self.filter['rectangle']) or room.capacity < self.filter['event'].capacity:
                continue
            collision = False
            for event in self.event:
                if event.location is None or event.location != room.id:
                    continue
                for period in event.getTimePeriod():
                    if Query.collide(period, (self.filter['start'], self.filter['end'])):
                        collision = True
                        break
            if not collision:
                yield room
        return
                





    