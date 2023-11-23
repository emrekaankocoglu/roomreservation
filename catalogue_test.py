import unittest
from room.room import Room
from event.event import Event
from catalogue.catalogue import Catalogue
from organization.organization import Organization
from user.user import User
from datetime import datetime, timedelta
from datetime import time
from view.view import View

class TestCatalogue(unittest.TestCase):
    def setUp(self):
        # Instantiate Catalogue before each test case
        self.catalogue = Catalogue()

    def test_registerRoom(self):
        name = "Sample Location"
        x = 30 
        y = 40  
        capacity = 100
        working_hours = (time(0, 0), time(17, 0))
        permissions = {
            User: ["PERWRITE", "WRITE"]
        }
        room = Room.create(name,x,y, capacity, working_hours, permissions)
        room_id = self.catalogue.registerRoom(room)
        self.assertEqual(self.catalogue.rooms[room_id].name, "Sample Location")

    def test_registerEvent(self):
        title = "Sample Event"
        description = "This is a sample event description."
        category = "Workshop"
        capacity = 50
        duration = timedelta(hours=2, minutes=30) 
        weekly = datetime.now() + timedelta(days=14)
        permissions = {
            User: ["PERWRITE", "WRITE"]
        }
        event = Event.create(title, description, category, capacity, duration, weekly, permissions)
        event_id = self.catalogue.registerEvent(event)
        self.assertEqual(self.catalogue.events[event_id].title, "Sample Event")
    """
    def test_registerOrganization(self):
        user2 = User(2,"Alice", "y@gmail.com", "Alice denis", "2345")
        org = Organization.create(user2.id,"IEEE",None,{},{})
        org_id = self.catalogue.registerOrganization(Organization("Org1"))
        self.assertEqual(self.catalogue.organizations[org_id].name, "Org1")
    """
    def test_listobject(self):

        title = "Sample Event"
        description = "This is a sample event description."
        category = "Workshop"
        capacity = 50
        duration = timedelta(hours=2, minutes=30) 
        weekly = datetime.now() + timedelta(days=14)
        permissions = {
            User: ["PERWRITE", "WRITE"]
        }

        name = "Sample Location"
        x = 30 
        y = 40  
        capacity = 100
        working_hours = (time(0, 0), time(17, 0))
        permissions = {
            User: ["PERWRITE", "WRITE"]
        }
        user2 = User(2,"Alice", "y@gmail.com", "Alice denis", "2345")
        room = Room.create(name,x,y, capacity, working_hours, permissions)
        event = Event.create(title, description, category, capacity, duration, weekly, permissions)
        org = Organization.create(user2.id,"IEEE",None,{},{})

        room_id = self.catalogue.registerRoom(room)
        event_id = self.catalogue.registerEvent(event)
        org_id = self.catalogue.registerOrganization(org)

        objects = self.catalogue.listobject()

        # Ensure the objects are present in the list
        self.assertTrue(any(obj['id'] == room_id and obj['name'] == "Sample Location" for obj in objects))
        self.assertTrue(any(obj['id'] == event_id and obj['name'] == "Sample Event" for obj in objects))
        self.assertTrue(any(obj['id'] == org_id and obj['name'] == "IEEE" for obj in objects))

    def test_getid(self):
        title = "Sample Event"
        description = "This is a sample event description."
        category = "Workshop"
        capacity = 50
        duration = timedelta(hours=2, minutes=30) 
        weekly = datetime.now() + timedelta(days=14)
        permissions = {
            User: ["PERWRITE", "WRITE"]
        }

        name = "Sample Location"
        x = 30 
        y = 40  
        capacity = 100
        working_hours = (time(0, 0), time(17, 0))
        permissions = {
            User: ["PERWRITE", "WRITE"]
        }
        user2 = User(2,"Alice", "y@gmail.com", "Alice denis", "2345")
        room = Room.create(name,x,y, capacity, working_hours, permissions)
        event = Event.create(title, description, category, capacity, duration, weekly, permissions)
        org = Organization.create(user2.id,"IEEE",None,{},{})

        room_id = self.catalogue.registerRoom(room)
        event_id = self.catalogue.registerEvent(event)
        org_id = self.catalogue.registerOrganization(org)

        self.assertEqual(self.catalogue.getid(room_id).name, "Sample Location")
        self.assertEqual(self.catalogue.getid(event_id).title, "Sample Event")
        self.assertEqual(self.catalogue.getid(org_id).name, "IEEE")

    def test_attach(self):
        title = "Sample Event"
        description = "This is a sample event description."
        category = "Workshop"
        capacity = 50
        duration = timedelta(hours=2, minutes=30) 
        weekly = datetime.now() + timedelta(days=14)
        permissions = {
            User: ["PERWRITE", "WRITE"]
        }

        name = "Sample Location"
        x = 30 
        y = 40  
        capacity = 100
        working_hours = (time(0, 0), time(17, 0))
        permissions = {
            User: ["PERWRITE", "WRITE"]
        }
        
        room = Room.create(name,x,y, capacity, working_hours, permissions)
        event = Event.create(title, description, category, capacity, duration, weekly, permissions)
        room_id = self.catalogue.registerRoom(room)
        event_id = self.catalogue.registerEvent(event)

        self.assertEqual(self.catalogue.attach(room_id).name, "Sample Location")
        self.assertEqual(self.catalogue.attach(event_id).title, "Sample Event")

    def test_registerUser(self):
        user = User(4,"Alice", "y@gmail.com", "Alice denis", "2345")
        self.assertEqual(self.catalogue.registerUser(user), user)
        self.assertEqual(self.catalogue.user, user)

    def test_switchuser(self):
        user1 = User(1,"John", "x@gmail.com", "John Doe", "1234")
        user2 = User(2,"Alice", "y@gmail.com", "Alice denis", "2345")

        self.catalogue.registerUser(user1)
        self.assertEqual(self.catalogue.switchuser(user2), user2)
        self.assertEqual(self.catalogue.user, user2)

    def test_getUser(self):
        user = User(3,"John", "x@gmail.com", "John Doe", "1234")
        with self.assertRaises(Exception):
            self.catalogue.getUser()  # Should raise an exception since no user is logged in

        self.catalogue.registerUser(user)
        self.assertEqual(self.catalogue.getUser(), user)


if __name__ == "__main__":
    unittest.main()