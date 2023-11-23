import unittest
from room.room import Room
from event.event import Event
from catalogue.catalogue import Catalogue
from organization.organization import Organization
from user.user import User
import datetime
import time
from view.view import View

class TestEvent(unittest.TestCase):
    def setUp(self):
        self.catalogue = Catalogue()

    def test_create_event(self):
        event = Event.create("Title", "Description", "Category", 10, datetime.timedelta(hours=1), None, {})
        self.assertIsInstance(event, Event)
        self.assertIn(event.id, self.catalogue.events)

    def test_get_event(self):
        event = Event.create("Title", "Description", "Category", 10, datetime.timedelta(hours=1), None, {})
        retrieved_event = Event.get(event.id)
        self.assertEqual(retrieved_event, event)

    def test_update_event(self):
        event = Event.create("Title", "Description", "Category", 10, datetime.timedelta(hours=1), None, {})
        updated_event = event.update(title="New Title", description="New Description")
        self.assertEqual(updated_event.title, "New Title")
        self.assertEqual(updated_event.description, "New Description")
    """
    def test_assign_period(self):
        name = "Sample Location"
        x = 30 
        y = 40  
        capacity = 100
        working_hours = (time(0, 0), time(17, 0))
        permissions = {
            User: ["PERWRITE", "WRITE"]
        }
        
        room = Room.create(name,x,y, capacity, working_hours, permissions)
        self.catalogue.registerRoom(room)
        event = Event.create("Title", "Description", "Category", 10, datetime.timedelta(hours=1), None, {})
        self.catalogue.registerUser(User("User1"))

        with self.assertRaises(Exception):
            # User does not have permission to assign event
            event.assignPeriod(datetime.datetime.now(), room)

        # Mock user permissions to assign event and room
        event.permissions[self.catalogue.getUser().id] = ["PERWRITE"]
        room.permissions[self.catalogue.getUser().id] = ["WRITE"]

        event.assignPeriod(datetime.datetime.now(), room)
        self.assertIsNotNone(event.start)
        self.assertEqual(event.location, room.id)
    """
    """
    def test_get_time_period(self):
        start_time = datetime.datetime(2023, 11, 1, 10, 0, 0)
        event = Event.create("Title", "Description", "Category", 10, datetime.timedelta(hours=1), start_time, {})
        periods = list(event.getTimePeriod())

        self.assertTrue(len(periods) > 0)
        for period in periods:
            self.assertIsInstance(period, tuple)
            self.assertEqual(len(period), 2)
            self.assertIsInstance(period[0], datetime.datetime)
            self.assertIsInstance(period[1], datetime.datetime)
    """
if __name__ == "__main__":
    unittest.main()