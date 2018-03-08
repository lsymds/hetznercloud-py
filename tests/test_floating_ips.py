from hetznercloud import FLOATING_IP_TYPE_IPv4, SERVER_STATUS_RUNNING
from tests.base import BaseHetznerTest


class TestFloatingIps(BaseHetznerTest):
    def test_can_create_a_floating_ip(self):
        floating_ip = self.create_floating_ip("Test description")

        self.assertIsNotNone(floating_ip)
        self.assertEqual(floating_ip.description, "Test description")

    def test_can_assign_and_unassign_a_floating_ip_to_a_server(self):
        server, _ = self.create_server("test-assign-and-unassign-floating-ips")
        server.wait_until_status_is(SERVER_STATUS_RUNNING)
        
        floating_ip = self.create_floating_ip("Test description")

        floating_ip.assign_to_server(server.id)
        self.assertEqual(floating_ip.server, server.id)

        floating_ip.unassign_from_server()
        self.assertEqual(floating_ip.server, 0)

    def test_can_change_description_of_a_floating_ip(self):
        floating_ip = self.create_floating_ip("Test description")
        floating_ip.change_description("My new description")

        self.assertEqual(floating_ip.description, "My new description")

    def test_can_change_reverse_dns_record(self):
        floating_ip = self.create_floating_ip("Test description")
        floating_ip.change_reverse_dns_entry(floating_ip.ptr_ips[0])