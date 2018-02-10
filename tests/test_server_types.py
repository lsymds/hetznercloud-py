from tests.base import BaseHetznerTest


class TestServerTypes(BaseHetznerTest):
    def test_can_get_all_server_types(self):
        sts = list(self.client.server_types().get_all())
        self.assertIsNotNone(sts)
        self.assertTrue(len(sts) > 0)

    def test_can_filter_server_types_by_name(self):
        sts = list(self.client.server_types().get_all(name="cx11"))
        self.assertIsNotNone(sts)
        self.assertTrue(len(sts) == 1)

    def test_can_get_server_type_by_id(self):
        st = self.client.server_types().get(1)

        self.assertTrue(st.id)
        self.assertTrue(st.name)
        self.assertTrue(st.description)
        self.assertTrue(st.country)
        self.assertTrue(st.city)
        self.assertTrue(st.latitude)
        self.assertTrue(st.longitude)