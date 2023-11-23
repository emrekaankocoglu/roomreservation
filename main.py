from room.room import Room
from event.event import Event
from catalogue.catalogue import Catalogue
from organization.organization import Organization
from user.user import User
from datetime import datetime, timedelta
from datetime import time
from view.view import View


"""

    This file is used to test the functionality of the system.
    It is not a part of the system itself.
    Following methods are not implementations and do not contain any logic.
    Other means of automated-manual testing (unittests, manual with interpreter) will be provided in the demo.
    
"""

def createOrganization():
    pass
def createEvent(user):
    title = "Sample Event"
    description = "This is a sample event description."
    category = "Workshop"
    capacity = 50
    duration = timedelta(hours=2, minutes=30) 
    weekly = datetime.now() + timedelta(days=14)
    permissions = {
        user: ["PERWRITE", "WRITE"]
    }
    event = Event.create(title, description, category, capacity, duration, weekly, permissions)
    return event

def createRoom(user):
    name = "3Sample Location"
    x = 30 
    y = 40  
    capacity = 100
    working_hours = (time(0, 0), time(17, 0))
    permissions = {
        user: ["PERWRITE", "WRITE"]
    }
    room = Room.create(name,x,y, capacity, working_hours, permissions)
    return room

def retrieveOrganization(id):
    organization = Organization.retrieve(id)
    return organization
def retrieveEvent(id):
    event = Event.retrieve(id)
    return event
def retrieveRoom(id):
    room = Room.retrieve(id)
    return room

def updateOrganization(id,update_dict):
    organization = Organization.update(id,update_dict)
    return organization
def updateEvent(id, **kwargs):
    event = Event.update(id, **kwargs)
    return event
def updateRoom(id, **kwargs):
    room = Room.update(id, **kwargs)
    return room

def deleteOrganization(id):
    Organization.delete(id)
def deleteEvent(id):
    Event.delete(id)
def deleteRoom(id):
    Room.delete(id)

def createUser():
    user = User.createUser(0,"y","z","w","s",)
    return user



def main():
    #isSingleton
    cat = Catalogue()
    print(cat)
    cat2 = Catalogue()
    print(cat2)
    
    #switch user work
    user = createUser()
    user2 = User.createUser(1,"b","c","d","f")
    cat.switchuser(user)
    print(cat.switchuser(user))
    cat.switchuser(user2)
    print(cat.switchuser(user2))
    
    #crud on room
    a = createRoom(user2.id)
    print(a)
    aRet = retrieveRoom(a.id)
    print(aRet)
    aUp = updateRoom(a, **{'x':10})
    print(aUp.x)
    deleteRoom(a.id)
    

    #crud on event
    b = createEvent(user2.id)
    print(b)
    bRet = retrieveEvent(b.id)
    print(bRet)
    bUp = updateEvent(b, **{'title': 'Not Sample Event'})
    print(bUp)
    deleteEvent(b.id)
    
    #methods on organization
    
    org = Organization.create(user2.id,"IEEE",None,{},{})
    print(org)
    org.registerRoom(a)
    org.registerEvent(b)
    print(org)
    org.reassign(b,a,datetime.now()+timedelta(days=1))
     
    org.findSchedule([v for v in org.events.values()], ((0,0), (100,100)), datetime.now(), datetime.now()+timedelta(days=2))
    
    """
    b = createEvent(user.id)
    c = Organization.create(user.id,"IEEE",None,{},{})
    c.registerRoom(a)
    c.registerEvent(b)
    c.reserve(b,a,datetime.now())
    b = createEvent(user.id)
    a = createRoom(user.id)
    b = createEvent(user.id)
    c.registerRoom(a)
    c.registerEvent(b)
    c.reserve(b,a,datetime.now()+timedelta(days=1))
    c.findSchedule([v for v in c.events.values()], ((0,0), (100,100)), datetime.now(), datetime.now()+timedelta(days=2))
    n=c.findScheduleInterval([v for v in c.events.values()], ((0,0), (100,100)), datetime.now(), datetime.now()+timedelta(minutes=350), timedelta(minutes=30))
    user.view = View(user.id)
    query_filter = {
        "title" : "S",
        "category" : "Workshop",
        "start": datetime.now(),
        "end": datetime.now()+timedelta(days=2),
        "rectangle": ((0,0),(100,100))
    }
    user.view.addquery(c.id, **query_filter)
    user.view.dayView(datetime.now(), datetime.now()+timedelta(days=2))
    user.view.roomView(datetime.now(), datetime.now()+timedelta(days=2))
    user.view.delquery(1)
    """

if __name__=="__main__": 
    main() 