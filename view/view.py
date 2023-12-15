from catalogue.catalogue import Catalogue
from catalogue.object import Object
from query.query import Query

class View(Object):
    def __init__(self, owner:id):
        Object.__init__(self)
        self.owner = owner
        self.queryset = {}
        self.obj_count = 0
    def addquery(self, organization, **kwargs):
        self.obj_count += 1
        id = self.obj_count
        obj_dict = {
            id: (kwargs, organization)
        }
        self.queryset.update(obj_dict)
        return self.queryset[id]
    def delquery(self, qid):
        del self.queryset[qid]
        return qid
    def roomView(self, start, end):
        queries = [Query(v[0], Catalogue().organizations[v[1]].rooms, Catalogue().organizations[v[1]].events) for k,v in self.queryset.items()]
        results = []
        for q in queries:
            for result in q.queryIterator():
                results.append(result)
        rooms = {}
        for event, room, s in results:
            if s >= start and s+event.duration <= end:
                if room.name not in rooms:
                    rooms[room.name] = []
                rooms[room.name].append((event, s))
        return rooms
    def dayView(self, start, end):
        queries = (Query(v[0], Catalogue().organizations[v[1]].rooms, Catalogue().organizations[v[1]].events) for k,v in self.queryset.items())
        results = []
        for query in queries:
            results += [result for result in query.queryIterator()]
        days = {}
        for event, room, s in results:
            if s >= start and s+event.duration <= end:
                if s.date() not in days:
                    days[s.date()] = []
                days[s.date()].append((event, room))
        return days

