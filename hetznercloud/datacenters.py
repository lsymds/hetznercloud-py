from .exceptions import HetznerActionException
from .shared import _get_results


class HetznerCloudDatacentersAction(object):
    """
    This action contains all functionality related to datacenters within the Hetzner Cloud service.
    """

    def __init__(self, config):
        """
        Initialises a new instance of the HetznerCloudDatacentersAction.

        :param config: A HetznerCloudClientConfiguration object.
        """
        self._config = config

    def get_all(self, name=None):
        """
        Gets all of the datacenters available on the Hetzner Cloud service.

        :param name: The optional name to filter the datacenters by.
        :return: An array of datacenters.
        """
        status_code, results = _get_results(self._config, "datacenters",
                                            url_params={"name": name} if name is not None else None)
        if status_code != 200:
            raise HetznerActionException(results)

        for result in results["datacenters"]:
            yield HetznerCloudDatacenter._load_from_json(result)

    def get(self, id):
        """
        Gets a specific datacenter by its id.

        :param id: The id of the datacenter to retrieve.
        :return: The HetznerCloudDatacenter object.
        """
        status_code, results = _get_results(self._config, "datacenters/%s" % id, method="GET")
        if status_code != 200:
            raise HetznerActionException(results)

        return HetznerCloudDatacenter._load_from_json(results["datacenter"])


class HetznerCloudDatacenter(object):
    """
    Represents a datacenter that exists in the Hetzner Cloud service.
    """

    def __init__(self):
        """
        Initialises a new instance of the HetznerCloudDatacenter class.
        """
        self.id = 0
        self.name = ""
        self.description = ""
        self.location_id = 0
        self.supported_server_types = []
        self.available_server_types = []

    @staticmethod
    def _load_from_json(json):
        dc = HetznerCloudDatacenter()

        dc.id = json["id"]
        dc.name = json["name"]
        dc.description = json["description"]
        dc.location_id = json["location"]["id"]
        dc.supported_server_types = json["server_types"]["supported"]
        dc.available_server_types = json["server_types"]["available"]

        return dc
