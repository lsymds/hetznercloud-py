from __future__ import absolute_import
from tests.base import BaseHetznerTest


class TestLocations(BaseHetznerTest):
    def test_can_get_all_locations(self):
        locations = list(self.client.locations().get_all())
        self.assertIsNotNone(locations)
        self.assertTrue(len(locations) > 0)

    def test_can_filter_locations_by_name(self):
        locations = list(self.client.locations().get_all(name="fsn1"))
        self.assertIsNotNone(locations)
        self.assertTrue(len(locations) == 1)

    def test_can_get_location_by_id(self):
        location = self.client.locations().get(1)

        self.assertTrue(location.id)
        self.assertTrue(location.name)
        self.assertTrue(location.description)
        self.assertTrue(location.country)
        self.assertTrue(location.city)
        self.assertTrue(location.latitude)
        self.assertTrue(location.longitude)