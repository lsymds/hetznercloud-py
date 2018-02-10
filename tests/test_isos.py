from tests.base import BaseHetznerTest


class TestIsos(BaseHetznerTest):
    def test_can_get_all_isos(self):
        isos = list(self.client.isos().get_all())
        self.assertIsNotNone(isos)
        self.assertTrue(len(isos) > 0)

    def test_can_filter_isos_by_name(self):
        isos = list(self.client.isos().get_all(name="virtio-win-0.1.141.iso"))
        self.assertIsNotNone(isos)
        self.assertTrue(len(isos) == 1)

    def test_can_get_iso_by_id(self):
        iso = self.client.isos().get(26)

        self.assertTrue(iso.id)
        self.assertTrue(iso.name)
        self.assertTrue(iso.description)
        self.assertTrue(iso.type)