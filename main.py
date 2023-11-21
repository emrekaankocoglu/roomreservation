from room.room import Room
from event.event import Event
from catalogue.catalogue import Catalogue
from organization.organization import Organization
from user.user import User

def createOrganization():
    organization = Organization.create("IEEE",[1,2,3],["Meetings","giving prizes"])
    return organization
def createEvent():
    event = Event.create()
    
def createRoom():
    room = Room.create()

def retrieveOrganization():
    pass
def retrieveEvent():
    pass
def retrieveRoom():
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
    pass

if __name__=="__main__": 
    main() 