from tests.base import BaseHetznerTest


class TestSshKeys(BaseHetznerTest):
    def test_can_create_a_ssh_key(self):
        ssh_key = self.client.ssh_keys().create("My SSH key", "abcdef==")
        self.assertIsNotNone(ssh_key)
        self.assertIsNotNone(ssh_key.id)

    def test_can_get_all_ssh_keys(self):
        self.client.ssh_keys().create("My ssh key", "abcdef==")

        ssh_keys = list(self.client.ssh_keys().get_all())
        self.assertEqual(len(ssh_keys), 1)

    def test_can_filter_ssh_keys_by_name(self):
        self.client.ssh_keys().create("My ssh key", "abcdef==")
        self.client.ssh_keys().create("My ssh key 2", "abcdef==")

        ssh_keys = list(self.client.ssh_keys().get_all(name="My ssh key 2"))
        self.assertEqual(len(ssh_keys), 1)

    def test_can_delete_ssh_key(self):
        ssh_key = self.client.ssh_keys().create("My ssh key", "abcdef==")
        ssh_key.delete()

    def test_can_update_ssh_key(self):
        ssh_key = self.client.ssh_keys().create("My ssh key", "abcdef==")
        ssh_key.update("A different SSH key")

        self.assertEquals(ssh_key.name, "A different SSH key")
