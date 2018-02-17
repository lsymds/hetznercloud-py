from .exceptions import HetznerActionException
from .shared import _get_results


class HetznerCloudIsosAction(object):
    def __init__(self, config):
        self._config = config

    def get_all(self, name=None):
        status_code, results = _get_results(self._config, "isos?per_page=100",
                                            url_params={"name": name} if name is not None else None)
        if status_code != 200:
            raise HetznerActionException(results)

        for result in results["isos"]:
            yield HetznerCloudIso._load_from_json(result)

    def get(self, id):
        status_code, results = _get_results(self._config, "isos/%s" % id)
        if status_code != 200:
            raise HetznerActionException(results)

        return HetznerCloudIso._load_from_json(results["iso"])


class HetznerCloudIso(object):
    def __init__(self):
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
