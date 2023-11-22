from user.user import User
import json
class Singleton:
    def __new__(cls,*a, **b):
        if hasattr(cls,'_inst'):
            return cls._inst
        else:
            cls._inst=super().__new__(cls,*a,**b)
            return cls._inst

class Catalogue(Singleton):
    def __init__(self):
        if not hasattr(self, 'id_counter'):
            self.id_counter = 0
            self.rooms = {}
            self.events = {}
            self.organizations = {}
            self.user = None

    
    def registerRoom(self, room):
        self.id_counter += 1
        id = self.id_counter
        room_dict = {
            id: room
        }
        self.rooms.update(room_dict)
        return self.id_counter
    def registerEvent(self, event):
        self.id_counter += 1
        id = self.id_counter
        event_dict = {
            id : event
        }
        self.events.update(event_dict)
        return self.id_counter
    def registerOrganization(self, organization):
        self.id_counter += 1
        id = self.id_counter
        organization_dict = {
            id : organization
        }
        self.organizations.update(organization_dict)
        return self.id_counter
    
    def listobject(self):
        return [{"id": k, "name": v.name} for k,v in Catalogue().rooms.items()] + \
        [{"id": k, "name": v.title} for k,v in Catalogue().events.items()] + \
        [{"id": k, "name": v.name} for k,v in Catalogue().organizations.items()]
    
    def getid(self, id):
        if id in self.rooms:
            return self.rooms[id]
        elif id in self.events:
            return self.events[id]
        elif id in self.organizations:
            return self.organizations[id]
        else:
            raise Exception("Object not found")
        
    def attach(self, id):
        if id in self.rooms:
            return self.rooms[id]
        elif id in self.events:
            return self.events[id]
        else:
            raise Exception("Object not found")
    def detach(self, id):
        pass # not required for this phase
    
    def registerUser(self, user):
        self.user = user
        return self.user
    def switchuser(self, user):
        self.user = user 
        return self.user
    def getUser(self):
        if self.user is None:
           raise Exception("No user logged in")
        return self.user
    