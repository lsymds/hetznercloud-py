from .exceptions import HetznerInvalidArgumentException, HetznerActionException
from .shared import _get_results


class HetznerCloudSSHKeysAction(object):
    def __init__(self, config):
        self._config = config

    def get_all(self, name=None):
        status_code, results = _get_results(self._config, "ssh_keys",
                                            url_params={"name": name} if name is not None else None)
        if status_code != 200:
            raise HetznerActionException(results)

        for result in results["ssh_keys"]:
            yield HetznerCloudSSHKey._load_from_json(self._config, result)

    def get(self, id):
        status_code, result = _get_results(self._config, "ssh_keys/%s" % id)
        if status_code != 200:
            raise HetznerActionException(result)

        return HetznerCloudSSHKey._load_from_json(self._config, result["ssh_key"])

    def create(self, name, public_key):
        if not name:
            raise HetznerInvalidArgumentException("name")
        if not public_key:
            raise HetznerInvalidArgumentException("public_key")

        status_code, result = _get_results(self._config, "ssh_keys", method="POST",
                                           body={"name": name, "public_key": public_key})
        if status_code != 201:
            raise HetznerActionException(result)

        return HetznerCloudSSHKey._load_from_json(self._config, result["ssh_key"])


class HetznerCloudSSHKey(object):
    def __init__(self, config):
        self._config = config
        self.id = 0
        self.name = ""
        self.fingerprint = ""
        self.public_key = ""

    def delete(self):
        status_code, result = _get_results(self._config, "ssh_keys/%s" % self.id, method="DELETE")
        if status_code != 201:
            raise HetznerActionException(result)

    def update(self, name):
        if not name:
            raise HetznerInvalidArgumentException("name")

        status_code, result = _get_results(self._config, "ssh_keys/%s" % self.id, method="PUT",
                                           body={"name": name})
        if status_code != 200:
            raise HetznerActionException(result)

        self.name = name

    @staticmethod
    def _load_from_json(config, json):
        ssh_key = HetznerCloudSSHKey(config)

        ssh_key.id = int(json["id"])
        ssh_key.name = json["name"]
        ssh_key.fingerprint = json["fingerprint"]
        ssh_key.public_key = json["public_key"]

        return ssh_key