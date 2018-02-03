import unittest

from hetznercloud import HetznerCloudClient
from .shared import valid_configuration


class BaseHetznerTest(unittest.TestCase):
    def setUp(self):
        self.client = HetznerCloudClient(valid_configuration)
        self.servers = self.client.servers()

    def tearDown(self):
        for server in self.servers.get_all():
            server.delete()