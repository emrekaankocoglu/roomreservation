from room.room import Room
from event.event import Event
from catalogue.catalogue import Catalogue
from organization.organization import Organization
from user.user import User
from datetime import datetime, timedelta
from datetime import time






def createOrganization():
    organization = Organization.create("IEEE",[1,2,3],["Meetings","giving prizes"])
    return organization

def createEvent():
    title = "Sample Event"
    description = "This is a sample event description."
    category = "Workshop"
    capacity = 50
    duration = timedelta(hours=2, minutes=30)
    start = datetime(2023, 11, 25, 15, 0)  
    weekly = datetime.now().date()  
    permissions = {
        "edit": True,
        "delete": False,
        "invite": True
    }
    event = Event.create(title, description, category, capacity, duration, weekly, permissions)
    return event

def createRoom():
    name = "Sample Location"
    x = 10 
    y = 20  
    capacity = 100
    working_hours = (time(9, 0), time(17, 0))
    permissions = {
        "edit": True,
        "delete": False,
        "manage_staff": True
    }
    room = Room.create(name,x,y, capacity, working_hours, permissions)
    return room

def retrieveOrganization():
    organization = Organization.retrieve(1)
    return organization
def retrieveEvent(id):
    event = Event.retrieve(1)
    return event
def retrieveRoom(id):
    
    pass

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
    user = User.createUser("x","y","z","w")
    return user

def switchUser():
    pass

def main():
    c = Catalogue()
    a = createRoom()
    b = Room.retrieve(a.id)
    print(b)

if __name__=="__main__": 
    main() 