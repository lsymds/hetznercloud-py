from .constants import IMAGE_TYPE_SNAPSHOT
from .exceptions import HetznerActionException
from .shared import _get_results


class HetznerCloudImagesAction(object):
    def __init__(self, config):
        self._config = config

    def get_all(self, sort=None, type=None, bound_to=None, name=None):
        url_params = {}
        if sort is not None:
            url_params["sort"] = sort
        if type is not None:
            url_params["type"] = type
        if bound_to is not None:
            url_params["bound_to"] = bound_to
        if name is not None:
            url_params["name"] = name

        status_code, results = _get_results(self._config, "images?per_page=100", url_params=url_params)
        if status_code != 200:
            raise HetznerActionException(results)

        for result in results["images"]:
            yield HetznerCloudImage._load_from_json(self._config, result)

    def get(self, id):
        status_code, results = _get_results(self._config, "images/%s" % id)
        if status_code != 200:
            raise HetznerActionException(results)

        return HetznerCloudImage._load_from_json(self._config, results["image"])


class HetznerCloudImage(object):
    def __init__(self, config):
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

    def update(self, description=None, type=None):
        body = {}
        if description is not None:
            body["description"] = description
        if type is not None:
            body["type"] = type

        status_code, result = _get_results(self._config, "images/%s" % self.id, method="PUT", body=body)
        if status_code != 200:
            raise HetznerActionException(result)

        self.description = description
        self.type = type

    def delete(self):
        status_code, result = _get_results(self._config, "images/%s" % self.id, method="DELETE")
        if status_code != 200:
            raise HetznerActionException(result)

    @staticmethod
    def _load_from_json(config, json):
        image = HetznerCloudImage(config)

        image.id = int(json["id"])
        image.type = json["type"]
        image.status = json["status"]
        image.name = json["name"]
        image.description = json["description"]
        image.image_size = float(json["image_size"]) if json["image_size"] is not None else None
        image.disk_size = float(json["disk_size"]) if json["disk_size"] is not None else None
        image.created_from_id = int(json["created_from"]["id"]) if json["created_from"] is not None else None
        image.created_from_name = json["created_from"]["name"] if json["created_from"] is not None else None
        image.bound_to = int(json["bound_to"]) if json["bound_to"] is not None else None
        image.os_flavor = json["os_flavor"]
        image.os_version = json["os_version"]
        image.rapid_deploy = bool(json["rapid_deploy"])

        return image
