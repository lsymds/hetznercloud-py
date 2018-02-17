from .exceptions import HetznerActionException
from .shared import _get_results


class HetznerCloudLocationsAction(object):
    def __init__(self, config):
        self._config = config

    def get_all(self, name=None):
        status_code, results = _get_results(self._config, "locations",
                                            url_params={"name": name} if name is not None else None)
        if status_code != 200:
            raise HetznerActionException(results)

        for result in results["locations"]:
            yield HetznerCloudLocation._load_from_json(result)

    def get(self, id):
        status_code, results = _get_results(self._config, "locations/%s" % id, method="GET")
        if status_code != 200:
            raise HetznerActionException(results)

        return HetznerCloudLocation._load_from_json(results["location"])


class HetznerCloudLocation(object):
    def __init__(self):
        self.id = 0
        self.name = ""
        self.description = ""
        self.country = ""
        self.city = ""
        self.latitude = 0.0
        self.longitude = 0.0

    @staticmethod
    def _load_from_json(json):
        location = HetznerCloudLocation()

        location.id = int(json["id"])
        location.name = json["name"]
        location.description = json["description"]
        location.country = json["country"]
        location.city = json["city"]
        location.latitude = float(json["latitude"])
        location.longitude = float(json["longitude"])

        return location
