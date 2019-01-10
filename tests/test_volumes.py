from hetznercloud import SERVER_STATUS_RUNNING, VOLUME_STATUS_AVAILABLE, ACTION_STATUS_SUCCESS
from tests.base import BaseHetznerTest

MIN_VOLUME_SIZE = 10


class TestVolumes(BaseHetznerTest):
    def test_can_create_a_volume_in_location(self):
        volume, _ = self.create_volume(name = "test-can-create-a-volume-in-location", size = MIN_VOLUME_SIZE, location = "nbg1")

        self.assertIsNotNone(volume)
        self.assertIsNotNone(volume.id)
        self.assertEqual(volume.size, MIN_VOLUME_SIZE)

    def test_can_create_a_volume_with_server(self):
        server, _ = self.create_server("test-can-create-a-volume-with-server")
        server.wait_until_status_is(SERVER_STATUS_RUNNING)

        volume, _ = self.create_volume(name = "test-can-create-a-volume-with-server", size = MIN_VOLUME_SIZE, server_id = server.id)
        volume.wait_until_status_is(VOLUME_STATUS_AVAILABLE)

        volume.wait_until_server_is(server.id)

        self.assertEqual(volume.server_id, server.id)

    def test_can_resize_a_volume(self):
        volume, action = self.create_volume(name = "test-can-resize-a-volume", size = MIN_VOLUME_SIZE, location = "nbg1")
        action.wait_until_status_is(ACTION_STATUS_SUCCESS)

        action = volume.resize(MIN_VOLUME_SIZE * 2)
        action.wait_until_status_is(ACTION_STATUS_SUCCESS)

        self.assertEqual(volume.size, MIN_VOLUME_SIZE * 2)

    def test_can_attach_and_detach_a_volume_to_a_server(self):
        server, _ = self.create_server("test-can-attach-and-detach-a-volume-to-a-server")
        server.wait_until_status_is(SERVER_STATUS_RUNNING)

        volume, _ = self.create_volume(name = "test-can-attach-and-detach-a-volume-to-a-server", size = MIN_VOLUME_SIZE, location = "nbg1")
        volume.wait_until_status_is(VOLUME_STATUS_AVAILABLE)

        action = volume.attach_to_server(server.id)
        action.wait_until_status_is(ACTION_STATUS_SUCCESS)

        self.assertEqual(volume.server_id, server.id)

        action = volume.detach_from_server()
        action.wait_until_status_is(ACTION_STATUS_SUCCESS)

        self.assertEqual(volume.server_id, 0)
