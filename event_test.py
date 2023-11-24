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
    
if __name__ == "__main__":
    unittest.main()