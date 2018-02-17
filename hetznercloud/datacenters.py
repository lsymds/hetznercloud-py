from .exceptions import HetznerActionException
from .locations import HetznerCloudLocation
from .shared import _get_results


class HetznerCloudDatacentersAction(object):
    def __init__(self, config):
        self._config = config

    def get_all(self, name=None):
        status_code, results = _get_results(self._config, "datacenters",
                                            url_params={"name": name} if name is not None else None)
        if status_code != 200:
            raise HetznerActionException(results)

        for result in results["datacenters"]:
            yield HetznerCloudDatacenter._load_from_json(result)

    def get(self, id):
        status_code, results = _get_results(self._config, "datacenters/%s" % id)
        if status_code != 200:
            raise HetznerActionException(results)

        return HetznerCloudDatacenter._load_from_json(results["datacenter"])


class HetznerCloudDatacenter(object):
    def __init__(self):
        self.id = 0
        self.name = ""
        self.description = ""
        self.location = None
        self.supported_server_types = []
        self.available_server_types = []

    @staticmethod
    def _load_from_json(json):
        dc = HetznerCloudDatacenter()

        dc.id = int(json["id"])
        dc.name = json["name"]
        dc.description = json["description"]
        dc.location = HetznerCloudLocation._load_from_json(json["location"])
        dc.supported_server_types = json["server_types"]["supported"]
        dc.available_server_types = json["server_types"]["available"]

        return dc
