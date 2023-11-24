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
    
    # Add other test cases for other methods as required...

if __name__ == "__main__":
    unittest.main()