import time

from hetznercloud import STATUS_OFF
from tests.base import BaseHetznerTest


class TestServers(BaseHetznerTest):

    def test_all_servers_can_be_retrieved(self):
        server, action = self.servers.create("test-servers-can-be-retrieved", "cx11", "ubuntu-16.04")

        all_servers = list(self.servers.get_all())
        self.assertIsNotNone(all_servers)
        self.assertIsNot(0, len(all_servers))

    def test_servers_can_be_retrieved_by_name(self):
        server, _ = self.servers.create("test-servers-can-be-retrieved-by-name", "cx11", "ubuntu-16.04")

        filtered_servers = list(self.servers.get_all("test-servers-can-be-retrieved-by-name"))
        self.assertIsNotNone(filtered_servers)
        self.assertIs(1, len(filtered_servers))

    def test_server_can_be_created(self):
        created_server, _ = self.servers.create("test-server-can-be-created", "cx11", "ubuntu-16.04")

        self.assertIsNotNone(created_server)
        self.assertIsNotNone(created_server.id)
        self.assertEqual(created_server.name, "test-server-can-be-created")
        self.assertEqual(created_server.image_id, 1)
        self.assertEqual(created_server.server_type_id, 1)

    def test_server_can_be_created_but_offline(self):
        created_server, _ = self.servers.create("test-server-can-be-created-but-offline", "cx11", "ubuntu-16.04",
                                                start_after_create=False)

        self.assertIsNotNone(created_server)
        self.assertIsNotNone(created_server.id)

        for i in range(0, 10):
            server = list(self.servers.get_all(name="test-server-can-be-created-but-offline"))[0]
            if server.status == STATUS_OFF:
                return

            time.sleep(2)
            i += 1

        self.fail()
