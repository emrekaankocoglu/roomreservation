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



def updateOrganization():
    pass
def updateEvent():
    pass
def updateRoom():
    pass

def deleteOrganization():
    pass
def deleteEvent():
    pass
def deleteRoom():
    pass

def createUser():
    user = User.createUser("x","y","z","w","s",)
    return user

def switchUser():
    pass

def main():
    cat = Catalogue()
    user = createUser()
    cat.switchuser(user)
    a = createRoom(user.id)
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

if __name__=="__main__": 
    main() 