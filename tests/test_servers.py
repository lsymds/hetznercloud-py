from hetznercloud import SERVER_STATUS_OFF, ACTION_STATUS_SUCCESS, SERVER_STATUS_RUNNING, HetznerActionException
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
        created_server.wait_until_status_is(SERVER_STATUS_OFF)

    def test_rescue_mode_can_be_added_to_a_server(self):
        created_server, _ = self.servers.create("test-rescue-mode-can-be-added", "cx11", "ubuntu-16.04")
        created_server.wait_until_status_is(SERVER_STATUS_RUNNING)

        root_password, action = created_server.enable_rescue_mode()
        self.assertIsNotNone(root_password)
        action.wait_until_status_is(ACTION_STATUS_SUCCESS)

    def test_rescue_mode_can_be_disabled_on_a_server(self):
        created_server, _ = self.servers.create("test-rescue-mode-can-be-removed", "cx11", "ubuntu-16.04")
        created_server.wait_until_status_is(SERVER_STATUS_RUNNING)

        _, action = created_server.enable_rescue_mode()
        action.wait_until_status_is(ACTION_STATUS_SUCCESS)

        action = created_server.disable_rescue_mode()
        action.wait_until_status_is(ACTION_STATUS_SUCCESS)

    def test_can_rename_a_server(self):
        created_server, _ = self.servers.create("test-server-rename", "cx11", "ubuntu-16.04")
        created_server.wait_until_status_is(SERVER_STATUS_RUNNING)

        created_server.change_name("renamed-server")
        self.assertEqual(created_server.name, "renamed-server")

        renamed_server = self.servers.get(created_server.id)
        self.assertEqual(renamed_server.name, "renamed-server")
