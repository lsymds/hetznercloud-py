import unittest

from hetznercloud import HetznerCloudClient, SERVER_TYPE_1CPU_2GB, IMAGE_UBUNTU_1604
from .shared import valid_configuration


class BaseHetznerTest(unittest.TestCase):
    def setUp(self):
        self.client = HetznerCloudClient(valid_configuration)
        self.servers = self.client.servers()

    def tearDown(self):
        for server in self.servers.get_all():
            server.delete()
        for ssh_key in self.client.ssh_keys().get_all():
            ssh_key.delete()

    def create_server(self, name, start_after_create=True):
        return self.servers.create(name, SERVER_TYPE_1CPU_2GB, IMAGE_UBUNTU_1604, start_after_create=start_after_create)
