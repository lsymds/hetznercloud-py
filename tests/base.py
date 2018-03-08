import unittest

from hetznercloud import HetznerCloudClient, SERVER_TYPE_1CPU_2GB, IMAGE_UBUNTU_1604, FLOATING_IP_TYPE_IPv4
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
        for ip in self.client.floating_ips().get_all():
            ip.delete()

    def create_server(self, name, start_after_create=True):
        return self.servers.create(name, SERVER_TYPE_1CPU_2GB, IMAGE_UBUNTU_1604, start_after_create=start_after_create)

    def create_floating_ip(self, description):
        return self.client.floating_ips().create(FLOATING_IP_TYPE_IPv4, home_location=1, description=description)