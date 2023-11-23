import unittest
from catalogue.catalogue import Catalogue
from room.room import Room
from event.event import Event
from query.query import Query
import datetime
from organization.organization import Organization

class TestOrganization(unittest.TestCase):
    def setUp(self):
        self.catalogue = Catalogue()

    def test_create_organization(self):
        organization = Organization.create(1, "Org1", "Map1", {}, {})
        self.assertIsInstance(organization, Organization)
        self.assertIn(organization.id, self.catalogue.organizations)

    def test_get_organization(self):
        organization = Organization.create(1, "Org1", "Map1", {}, {})
        retrieved_organization = Organization.get(organization.id)
        self.assertEqual(retrieved_organization, organization)

    def test_update_organization(self):
        organization = Organization.create(1, "Org1", "Map1", {}, {})
        Organization.update(organization.id, name="New Org")
        self.assertEqual(organization.name, "New Org")
    """
    def test_reserve_event(self):
        organization = Organization.create(1, "Org1", "Map1", {}, {})
        room = Room.create("Room1", 0, 0, 20, (datetime.time(8, 0), datetime.time(18, 0)), {})
        event = Event.create("Event1", "Description", "Category", 10, datetime.timedelta(hours=1), None, {})
        start_time = datetime.datetime.now()

        organization.reserve(event, room, start_time)
        self.assertEqual(event.location, room.id)
        self.assertEqual(event.start, start_time)

    def test_reassign_event(self):
        organization = Organization.create(1, "Org1", "Map1", {}, {})
        room1 = Room.create("Room1", 0, 0, 20, (datetime.time(8, 0), datetime.time(18, 0)), {})
        room2 = Room.create("Room2", 0, 0, 20, (datetime.time(8, 0), datetime.time(18, 0)), {})
        event = Event.create("Event1", "Description", "Category", 10, datetime.timedelta(hours=1), None, {})
        start_time = datetime.datetime.now()

        organization.reserve(event, room1, start_time)
        organization.reassign(event, room2, start_time)
        self.assertEqual(event.location, room2.id)
        self.assertEqual(event.start, start_time)
    """
    # Add other test cases for other methods as required...

if __name__ == "__main__":
    unittest.main()