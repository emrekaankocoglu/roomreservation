from room.room import Room
from event.event import Event
from catalogue.catalogue import Catalogue
from organization.organization import Organization
from user.user import User
from datetime import datetime, timedelta
from datetime import time
from view.view import View
import sqlite3


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

def createUser2():
    user = User.createUser(2,"y","z","w","s",)
    return user

def switchUser():
    pass

def main():
    cat = Catalogue()
    try:
        User.createtable()
    except sqlite3.OperationalError:
        pass
    user = createUser()

    user_emre = User.createUser(3,"emre","e@e.com","emre kocoglu","emre")
    user_furkan = User.createUser(4,"furkan","f@f.com","fba","furkan")
    user_noone = User.createUser(5,"noone","n@n.com","no one","noone")
    user_emre.makeAdmin()
    user_furkan.makeAdmin()

    a = createRoom(user.username)
    b = createEvent(user.username)
    permissions = {
        "noone" : ["listEvent", "listRoom", "createRoom", "createEvent"],
    }
    c = Organization.create(user.username,"IEEE",None,{},{},permissions)
    c.registerRoom(a)
    c.registerEvent(b)
    try:
        user2 = createUser2()
        c.reserve(b,a,datetime.now()
                  )
    except Exception as e:
        print("failed: ", e)
    # print("assigned event:", c.reserve(b,a,datetime.now(), user.username))
    b = createEvent(user.
                    id)
    
    a = createRoom(user.id)
    b = createEvent(user.id)
    c.registerRoom(a)
    c.registerEvent(b)
    print("assign another")
    # print(c.reserve(b,a,datetime.now()+timedelta(days=7), user.username))
    print("find schedule")
    print(c.findSchedule([v for v in c.events.values()], ((0,0), (100,100)), datetime.now(), datetime.now()+timedelta(days=2)))
    n=c.findScheduleInterval([v for v in c.events.values()], ((0,0), (100,100)), datetime.now(), datetime.now()+timedelta(minutes=350), timedelta(minutes=30))
    print("find schedule interval")
    print(n)
    user.view = View(user.username)
    query_filter = {
        "title" : "S",
        "category" : "Workshop",
        "start": datetime.now(),
        "end": datetime.now()+timedelta(days=2),
        "rectangle": ((0,0),(100,100))
    }
    print("user view")
    user.view.addquery(c.id, **query_filter)
    print(user.view.dayView(datetime.now()-timedelta(days=1), datetime.now()+timedelta(days=2)))
    print(user.view.roomView(datetime.now()-timedelta(days=1), datetime.now()+timedelta(days=2)))
    user.view.delquery(1)
    print(user.view)
    return cat

if __name__=="__main__": 
    main() 