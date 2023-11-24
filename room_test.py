import unittest
from catalogue.catalogue import Catalogue
from room.room import Room
import datetime
from event.event import Event
from user.user import User
from datetime import datetime, timedelta
from datetime import time
class TestRoom(unittest.TestCase):
    def setUp(self):
        self.catalogue = Catalogue()
        user = User(3,"John", "x@gmail.com", "John Doe", "1234")
        self.catalogue.user = user

    def test_create_room(self):
        name = "Sample Location"
        x = 30 
        y = 40  
        capacity = 100
        working_hours = (time(0, 0), time(17, 0))
        permissions = {
            User: ["PERWRITE", "WRITE"]
        }
        
        room = Room.create(name,x,y, capacity, working_hours, permissions)
        self.assertIsInstance(room, Room)
        self.assertIn(room.id, self.catalogue.rooms)

    def test_get_room(self):
        name = "Sample Location"
        x = 30 
        y = 40  
        capacity = 100
        working_hours = (time(0, 0), time(17, 0))
        permissions = {
            User: ["PERWRITE", "WRITE"]
        }
        
        room = Room.create(name,x,y, capacity, working_hours, permissions)
        retrieved_room = Room.get(room.id)
        self.assertEqual(retrieved_room, room)

    def test_update_room(self):
        name = "Sample Location"
        x = 30 
        y = 40  
        capacity = 100
        working_hours = (time(0, 0), time(17, 0))
        permissions = {
            User: ["PERWRITE", "WRITE"]
        }
        
        room = Room.create(name,x,y, capacity, working_hours, permissions)
        updated_room = room.update(name="New Room", capacity=30)
        self.assertEqual(updated_room.name, "New Room")
        self.assertEqual(updated_room.capacity, 30)
   

if __name__ == "__main__":
    unittest.main()