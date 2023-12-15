from room.room import Room
from event.event import Event
import datetime
from catalogue.catalogue import Catalogue
from catalogue.object import Object
import copy

class Query(Object):
    def __init__(self, filter:dict, rooms:{}, events:{}):
        super().__init__()
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
        for room_id,room in self.rooms.items():
            if not Query.in_rectangle(room.x, room.y, self.filter['rectangle']) \
                or room.capacity < self.filter['event'].capacity \
                or self.filter['start'].time() < room.workinghours[0] \
                or self.filter['end'].time() > room.workinghours[1] \
                or self.filter['start'].time() > room.workinghours[1] \
                or self.filter['end'].time() < room.workinghours[0]:
                continue
            collision = False
            for event_id,event in self.events.items():
                if event.location is None or event.location != room.id:
                    continue
                for period in event.getTimePeriod():
                    temp = copy.deepcopy(self.filter['event'])
                    temp.start = self.filter['start']
                    temp.duration = self.filter['end'] - self.filter['start']
                    for period_reserve in temp.getTimePeriod():
                        if Query.collide(period, period_reserve):
                            collision = True
                            break
            if not collision:
                yield room
        return
    def queryIterator(self):
        for event_id, event in self.events.items():
            if event.location is None:
                continue
            if (self.filter.get('title') is not None and self.filter.get('title') in event.title) or (self.filter.get('category') is not None and self.filter['category'] in event.category):
                if self.filter.get('room') is not None: 
                    if event.location == self.filter['room'].id:
                        yield (event, self.filter['room'], event.start)
                elif self.filter.get('rectangle') is not None:
                    room = Catalogue().rooms[event.location]
                    if Query.in_rectangle(room.x, room.y, self.filter['rectangle']):
                        yield (event, room, event.start)
        return
    def constructSchedule(self):
        events = self.filter['eventlist']
        self.filter['event'] = events[0]
        results = []
        for room in self.findRoom():
            room_results = []
            q = copy.deepcopy(self)
            q.filter['event'].location = room.id
            q.filter['event'].start = self.filter['start']
            q.filter['eventlist'].remove(q.filter['event'])
            if len(q.filter['eventlist']) == 0:
                room_results.append([(self.filter['event'].id,room.id,self.filter['start'])])
            else:
                for q in q.constructSchedule():
                    room_results.append([(self.filter['event'].id,room.id,self.filter['start'])] + [q])
            results += room_results

        return results
    def constructIntervalSchedule(self):
        events = self.filter['eventlist']
        self.filter['event'] = events[0]
        results = []
        interval = self.filter['interval']
        start_time = self.filter['start']
        origin = self.filter['start']
        while start_time + self.filter['event'].duration < self.filter['end']:
            start_time = start_time + interval
            self.filter['start'] = start_time
            for room in self.findRoom():
                room_results = []
                q = copy.deepcopy(self)
                q.filter['start'] = origin
                q.filter['event'].location = room.id
                q.filter['event'].start = start_time
                q.filter['eventlist'].remove(q.filter['event'])
                if len(q.filter['eventlist']) == 0:
                    room_results.append([(self.filter['event'].id,room.id,self.filter['start'])])
                else:
                    for q in q.constructIntervalSchedule():
                        room_results.append([(self.filter['event'].id,room.id,self.filter['start'])] + [q])
                results += room_results
        self.filter['start'] = origin

        return results


    





                





    