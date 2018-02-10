from .exceptions import HetznerActionException
from .shared import _get_results


class HetznerCloudLocationsAction(object):
    """
    This action contains all functionality related to locations within the Hetzner Cloud service.
    """

    def __init__(self, config):
        """
        Initialises a new instance of the HetznerCloudLocationsAction.

        :param config: A HetznerCloudClientConfiguration object.
        """
        self._config = config

    def get_all(self, name=None):
        """
        Gets all of the locations available on the Hetzner Cloud service.

        :param name: The optional name to filter the locations by.
        :return: A generator consisting of HetznerCloudLocation objects.
        """
        status_code, results = _get_results(self._config, "locations",
                                            url_params={"name": name} if name is not None else None)
        if status_code != 200:
            raise HetznerActionException(results)

        for result in results["locations"]:
            yield HetznerCloudLocation._load_from_json(result)

    def get(self, id):
        """
        Gets a specific location by its id.

        :param id: The id of the location to retrieve.
        :return: The HetznerCloudLocation object.
        """
        status_code, results = _get_results(self._config, "locations/%s" % id, method="GET")
        if status_code != 200:
            raise HetznerActionException(results)

        return HetznerCloudLocation._load_from_json(results["location"])


class HetznerCloudLocation(object):
    """
    Represents a location that exists in the Hetzner Cloud service.
    """

    def __init__(self):
        """
        Initialises a new instance of the HetznerCloudLocation class.
        """
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

        location.id = json["id"]
        location.name = json["name"]
        location.description = json["description"]
        location.country = json["country"]
        location.city = json["city"]
        location.latitude = json["latitude"]
        location.longitude = json["longitude"]

        return location
