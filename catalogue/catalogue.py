from user.user import User
class Singleton(object):
  def __new__(cls):
    if not hasattr(cls, 'instance'):
      cls.instance = super(Singleton, cls).__new__(cls)
    return cls.instance

    
class Catalogue(Singleton):
    def __init__(self):
        self.id_counter = 0
        self.rooms = {}
        self.events = {}
        self.organizations = {}
        self.user = None
    
    def registerRoom(self, room):
        self.id_counter += 1
        room_dict = {
            "id" : self.id_counter,
            "room" : room
        }
        self.rooms.update(room_dict)
        return self.id_counter
    def registerEvent(self, event):
        self.id_counter += 1
        event_dict = {
            "id" : self.id_counter,
            "event" : event
        }
        self.events.update(event_dict)
        return self.id_counter
    def registerOrganization(self, organization):
        self.id_counter += 1
        organization_dict = {
            "id" : self.id_counter,
            "organization" : organization
        }
        self.organizations.update(organization_dict)
        return self.id_counter
    
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
    