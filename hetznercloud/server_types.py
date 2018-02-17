from .exceptions import HetznerActionException
from .shared import _get_results


class HetznerCloudServerTypesAction(object):
    def __init__(self, config):
        self._config = config

    def get_all(self, name=None):
        status_code, results = _get_results(self._config, "server_types",
                                            url_params={"name": name} if name is not None else None)
        if status_code != 200:
            raise HetznerActionException(results)

        for result in results["server_types"]:
            yield HetznerCloudServerType._load_from_json(result)

    def get(self, id):
        status_code, results = _get_results(self._config, "server_types/%s" % id)
        if status_code != 200:
            raise HetznerActionException(results)

        return HetznerCloudServerType._load_from_json(results["server_type"])


class HetznerCloudServerType(object):
    def __init__(self):
        self.id = 0
        self.name = ""
        self.description = ""
        self.cores = 1
        self.memory = 1
        self.disk = 1
        self.storage_type = ""

    @staticmethod
    def _load_from_json(json):
        server_type = HetznerCloudServerType()

        server_type.id = json["id"]
        server_type.name = json["name"]
        server_type.description = json["description"]
        server_type.cores = int(json["cores"])
        server_type.memory = int(json["memory"])
        server_type.disk = int(json["disk"])
        server_type.storage_type = json["storage_type"]

        return server_type