from .exceptions import HetznerActionException
from .shared import _get_results


class HetznerCloudServerTypesAction(object):
    """
    This action contains all functionality related to server types in the Hetzner Cloud service.
    """
    def __init__(self, config):
        """
        Initialises a new instance of the HetznerCloudServerTypesAction.

        :param config: A HetznerCloudClientConfiguration object.
        """
        self._config = config

    def get_all(self, name=None):
        """
        Gets all of the server types available on the Hetzner Cloud service.

        :param name: The optional name to filter the server types by.
        :return: A generator of server types.
        """
        status_code, results = _get_results(self._config, "server_types",
                                            url_params={"name": name} if name is not None else None)
        if status_code != 200:
            raise HetznerActionException(results)

        for result in results["server_types"]:
            yield HetznerCloudServerType._load_from_json(result)

    def get(self, id):
        """
        Gets a specific server type by its id.

        :param id: The id of the server type to retrieve.
        :return: The HetznerCloudServerType object.
        """
        status_code, results = _get_results(self._config, "server_types/%s" % id, method="GET")
        if status_code != 200:
            raise HetznerActionException(results)

        return HetznerCloudServerType._load_from_json(results["server_type"])


class HetznerCloudServerType(object):
    """
    Represents a server type in the Hetzner Cloud service.
    """

    def __init__(self):
        """
        Initialises a new instance of the HetznerCloudServerType object.
        """
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