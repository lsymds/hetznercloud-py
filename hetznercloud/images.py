from .exceptions import HetznerActionException
from .shared import _get_results
from .constants import IMAGE_TYPE_SNAPSHOT


class HetznerCloudImagesAction(object):
    """
    This action contains all functionality related to images within the Hetzner Cloud service.
    """

    def __init__(self, config):
        """
        Initialises a new instance of the HetznerCloudImagesAction object.

        :param config: A HetznerCloudClientConfiguration object.
        """
        self._config = config

    def get_all(self, sort=None, type=None, bound_to=None, name=None):
        """
        Gets all of the images available to the authenticated user on the Hetzner Cloud service.

        :param sort: The parameter to sort by.
        :param type: The type of the image to sort by (options are "backup" or "snapshot").
        :param bound_to: The server the image is bound to.
        :param name: The optional name to filter the images by.
        :return: A generator that yields the images.
        """
        url_params = {}
        if sort is not None:
            url_params["sort"] = sort
        if type is not None:
            url_params["type"] = type
        if bound_to is not None:
            url_params["bound_to"] = bound_to
        if name is not None:
            url_params["name"] = name

        status_code, results = _get_results(self._config, "images", url_params=url_params)
        if status_code != 200:
            raise HetznerActionException(results)

        for result in results["images"]:
            yield HetznerCloudImage._load_from_json(result)

    def get(self, id):
        """
        Gets a specific image.

        :param id: The id of the image to retrieve.
        :return: The HetznerCloudImage that matches the id passed in to this method.
        """
        status_code, results = _get_results(self._config, "images/%s" % id)
        if status_code != 200:
            raise HetznerActionException(results)

        return HetznerCloudImage._load_from_json(results["image"])


class HetznerCloudImage(object):
    """
    Represents an image in the Hetzner Cloud service.
    """

    def __init__(self, config):
        """
        Initialises a new instance of the HetznerCloudImage object.

        :param config: A configuration object.
        """
        self._config = config
        self.id = 0
        self.type = ""
        self.status = ""
        self.name = ""
        self.description = ""
        self.image_size = 0
        self.disk_size = 0
        self.created_from_id = 0
        self.created_from_name = ""
        self.bound_to = ""
        self.os_flavor = ""
        self.os_version = ""
        self.rapid_deploy = False

    def update(self, description, type=IMAGE_TYPE_SNAPSHOT):
        pass

    def delete(self):
        pass

    @staticmethod
    def _load_from_json(config, json):
        image = HetznerCloudImage(config)

        image.id = int(json["id"])
        image.type = json["type"]
        image.status = json["status"]
        image.name = json["name"]
        image.description = json["description"]
        image.image_size = float(json["image_size"])
        image.disk_size = float(json["disk_size"])
        image.created_from_id = int(json["created_from"]["id"])
        image.created_from_name = json["created_from"]["name"]
        image.bound_to = int(json["bound_to"])
        image.os_flavor = json["os_flavor"]
        image.os_version = json["os_version"]
        image.rapid_deploy = bool(json["rapid_deploy"])

        return image
