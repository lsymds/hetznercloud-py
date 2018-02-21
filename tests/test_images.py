from tests.base import BaseHetznerTest


class TestImages(BaseHetznerTest):
    def test_can_get_all_images(self):
        images = list(self.client.images().get_all())
        self.assertIsNotNone(images)
        self.assertTrue(len(images) > 0)

    def test_can_get_image_by_id(self):
        pass