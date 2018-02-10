from tests.base import BaseHetznerTest


class TestDatacenters(BaseHetznerTest):
    def test_can_get_all_datacenters(self):
        dcs = list(self.client.datacentres().get_all())
        self.assertIsNotNone(dcs)
        self.assertTrue(len(dcs) > 0)

    def test_can_filter_datacenters_by_name(self):
        dcs = list(self.client.datacentres().get_all(name="fsn1-dc8"))
        self.assertIsNotNone(dcs)
        self.assertTrue(len(dcs) == 1)

    def test_can_get_dc_by_id(self):
        dc = self.client.datacentres().get(1)

        self.assertTrue(dc.id)
        self.assertTrue(dc.name)
        self.assertTrue(dc.description)
        self.assertIsNotNone(dc.location)
        self.assertTrue(len(dc.available_server_types) > 0)
        self.assertTrue(len(dc.supported_server_types) > 0)