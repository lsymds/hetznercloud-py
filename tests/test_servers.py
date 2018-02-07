from hetznercloud import SERVER_STATUS_OFF, ACTION_STATUS_SUCCESS, SERVER_STATUS_RUNNING, \
    BACKUP_WINDOW_10PM_2AM, HetznerActionException, SERVER_TYPE_2CPU_4GB, SERVER_TYPE_1CPU_2GB
from tests.base import BaseHetznerTest


class TestServers(BaseHetznerTest):

    def test_all_servers_can_be_retrieved(self):
        self.create_server("test-server-can-be-retrieved")

        all_servers = list(self.servers.get_all())
        self.assertIsNotNone(all_servers)
        self.assertIsNot(0, len(all_servers))

    def test_servers_can_be_retrieved_by_name(self):
        self.create_server("test-servers-can-be-retrieved-by-name")

        filtered_servers = list(self.servers.get_all("test-servers-can-be-retrieved-by-name"))
        self.assertIsNotNone(filtered_servers)
        self.assertIs(1, len(filtered_servers))

    def test_server_can_be_created(self):
        created_server, _ = self.create_server("test-server-can-be-created")

        self.assertIsNotNone(created_server)
        self.assertIsNotNone(created_server.id)
        self.assertEqual(created_server.name, "test-server-can-be-created")
        self.assertEqual(created_server.image_id, 1)
        self.assertEqual(created_server.server_type_id, 1)

    def test_server_can_be_created_but_offline(self):
        created_server, _ = self.create_server("test-server-can-be-created-offline", False)

        self.assertIsNotNone(created_server)
        self.assertIsNotNone(created_server.id)
        created_server.wait_until_status_is(SERVER_STATUS_OFF)

    def test_rescue_mode_can_be_added_to_a_server(self):
        created_server, _ = self.create_server("test-rescue-mode-can-be-added")
        created_server.wait_until_status_is(SERVER_STATUS_RUNNING)

        root_password, action = created_server.enable_rescue_mode()
        self.assertIsNotNone(root_password)
        action.wait_until_status_is(ACTION_STATUS_SUCCESS)

    def test_rescue_mode_can_be_disabled_on_a_server(self):
        created_server, _ = self.create_server("test-rescue-mode-can-be-removed")
        created_server.wait_until_status_is(SERVER_STATUS_RUNNING)

        _, action = created_server.enable_rescue_mode()
        action.wait_until_status_is(ACTION_STATUS_SUCCESS)

        action = created_server.disable_rescue_mode()
        action.wait_until_status_is(ACTION_STATUS_SUCCESS)

    def test_can_rename_a_server(self):
        created_server, _ = self.create_server("test-server-rename")
        created_server.wait_until_status_is(SERVER_STATUS_RUNNING)

        created_server.change_name("renamed-server")
        self.assertEqual(created_server.name, "renamed-server")

        renamed_server = self.servers.get(created_server.id)
        self.assertEqual(renamed_server.name, "renamed-server")

    def test_invalid_backup_window_results_in_an_exception_being_thrown(self):
        created_server, _ = self.create_server("test-backup-window-errors")
        created_server.wait_until_status_is(SERVER_STATUS_RUNNING)

        try:
            created_server.enable_backups("02-03")
            self.fail()
        except HetznerActionException:
            pass

    def test_can_enable_backups_with_a_valid_backup_window(self):
        created_server, _ = self.create_server("test-rescue-mode-can-be-enabled")
        created_server.wait_until_status_is(SERVER_STATUS_RUNNING)

        created_server.enable_backups(BACKUP_WINDOW_10PM_2AM)

        self.assertEquals(created_server.backup_window, BACKUP_WINDOW_10PM_2AM)

    def test_can_attach_iso_to_a_server(self):
        created_server, _ = self.create_server("test-can-attach-iso")
        created_server.wait_until_status_is(SERVER_STATUS_RUNNING)

        attach_iso_action = created_server.attach_iso("virtio-win-0.1.141.iso")
        attach_iso_action.wait_until_status_is(ACTION_STATUS_SUCCESS)

    def test_can_change_reverse_dns_of_a_server(self):
        created_server, _ = self.create_server("test-can-change-reverse-dns")
        created_server.wait_until_status_is(SERVER_STATUS_RUNNING)

        created_server.change_reverse_dns_entry(created_server.public_net_ipv4, "google.com")

    def test_can_change_server_type(self):
        created_server, _ = self.create_server("test-can-change-server-type")
        created_server.wait_until_status_is(SERVER_STATUS_RUNNING)

        action = created_server.change_type(SERVER_TYPE_2CPU_4GB, False)
        action.wait_until_status_is(ACTION_STATUS_SUCCESS)

        action = created_server.change_type(SERVER_TYPE_1CPU_2GB, False)
        action.wait_until_status_is(ACTION_STATUS_SUCCESS)


