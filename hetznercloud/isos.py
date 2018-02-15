from .exceptions import HetznerActionException
from .shared import _get_results


class HetznerCloudIsosAction(object):
    """
    This action contains all functionality related to isos within the Hetzner Cloud service.
    """

    def __init__(self, config):
        """
        Initialises a new instance of the HetznerCloudIsosAction class.

        :param config: A HetznerCloudClientConfiguration object.
        """
        self._config = config

    def get_all(self, name=None):
        """
        Gets all of the isos available on the Hetzner Cloud service.

        :param name: The optional name to filter the isos by.
        :return: A generator consisting of HetznerCloudIso objects.
        """
        status_code, results = _get_results(self._config, "isos?per_page=100",
                                            url_params={"name": name} if name is not None else None)
        if status_code != 200:
            raise HetznerActionException(results)

        for result in results["isos"]:
            yield HetznerCloudIso._load_from_json(result)

    def get(self, id):
        """
        Gets a specific iso by its id.

        :param id: The id of the iso to retrieve.
        :return: The HetznerCloudIso object.
        """
        status_code, results = _get_results(self._config, "isos/%s" % id)
        if status_code != 200:
            raise HetznerActionException(results)

        return HetznerCloudIso._load_from_json(results["iso"])


class HetznerCloudIso(object):
    """
    Represents an iso that exists in the Hetzner cloud service.
    """

    def __init__(self):
        """
        Initialises a new instance of the HetznerCloudIso class.
        """
        self.id = 0
        self.name = ""
        self.description = ""
        self.type = ""

    @staticmethod
    def _load_from_json(json):
        iso = HetznerCloudIso()

        iso.id = int(json["id"])
        iso.name = json["name"]
        iso.description = json["description"]
        iso.type = json["type"]

        return iso
