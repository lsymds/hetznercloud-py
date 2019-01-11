import time

from .actions import HetznerCloudAction
from .constants import VOLUME_FORMAT_XFS, VOLUME_FORMAT_EXT4, VOLUME_MINIMUM_SIZE
from .exceptions import HetznerInvalidArgumentException, HetznerActionException
from .locations import HetznerCloudLocation
from .shared import _get_results


def _get_volume_json(config, volume_id):
    status_code, result = _get_results(config, "volumes/%s" % volume_id)
    if not "volume" in result:
        raise HetznerActionException(result)

    return result["volume"]


class HetznerCloudVolumesAction(object):
    def __init__(self, config):
        self._config = config

    def create(self, name, size=VOLUME_MINIMUM_SIZE, automount=False, format=None, location=None, server_id=None):
        if size < VOLUME_MINIMUM_SIZE:
            raise HetznerInvalidArgumentException("size (%d) has to be greater than VOLUME_MINIMUM_SIZE (%d)" % (size, VOLUME_MINIMUM_SIZE))
        if location is None and server_id is None:
            raise HetznerInvalidArgumentException("location or server_id must be set")
        if automount and server_id is None:
            raise HetznerInvalidArgumentException("server_id must be set if automount is true")
        if format is not None and format != VOLUME_FORMAT_XFS and format != VOLUME_FORMAT_EXT4:
            raise HetznerInvalidArgumentException("invalid format")

        create_params = {
            "name":      name,
            "size":      size,
            "automount": automount
        }

        if format is not None:
            create_params["format"] = format
        if location is not None:
            create_params["location"] = location
        if server_id is not None:
            create_params["server"] = server_id

        status_code, results = _get_results(self._config, "volumes", method="POST", body=create_params)
        if status_code != 201:
            raise HetznerActionException(results)

        return HetznerCloudVolume._load_from_json(self._config, results["volume"]), \
               HetznerCloudAction._load_from_json(self._config, results["action"])

    def get_all(self):
        status_code, results = _get_results(self._config, "volumes")
        if status_code != 200:
            raise HetznerActionException(results)

        for result in results["volumes"]:
            yield HetznerCloudVolume._load_from_json(self._config, result)

    def get(self, id):
        status_code, result = _get_results(self._config, "volumes/%s" % id)
        if status_code != 200:
            raise HetznerActionException(result)

        return HetznerCloudVolume._load_from_json(self._config, result["volume"])


class HetznerCloudVolume(object):
    def __init__(self, config):
        self._config = config
        self.id = 0
        self.created = ""
        self.name = ""
        self.server_id = 0
        self.location = None
        self.size = 0
        self.linux_device = ""
        self.status = ""
        self.format = ""

    def attach_to_server(self, server_id):
        if not server_id:
            raise HetznerInvalidArgumentException("server_id")

        status_code, result = _get_results(self._config, "volumes/%s/actions/attach" % self.id, method="POST",
                                           body={"server": server_id})
        if status_code != 201:
            raise HetznerActionException(result)

        self.server_id = server_id

        return HetznerCloudAction._load_from_json(self._config, result["action"])

    def detach_from_server(self):
        status_code, result = _get_results(self._config, "volumes/%s/actions/detach" % self.id, method="POST")
        if status_code != 201:
            raise HetznerActionException(result)

        self.server_id = 0

        return HetznerCloudAction._load_from_json(self._config, result["action"])

    def resize(self, size):
        if not size:
            raise HetznerInvalidArgumentException("size not set")

        if size <= self.size:
            raise HetznerInvalidArgumentException("new size (%d) has to be greater than the current size (%d)" % (size, self.size))

        status_code, result = _get_results(self._config, "volumes/%s/actions/resize" % self.id,
                                           method="POST", body={"size": size})
        if status_code != 201:
            raise HetznerActionException(result)

        self.size = size

        return HetznerCloudAction._load_from_json(self._config, result["action"])

    def delete(self):
        status_code, result = _get_results(self._config, "volumes/%s" % self.id, method="DELETE")
        if status_code != 204:
            raise HetznerActionException(result)

    def _wait_until_attribute_is(self, object_attribute, request_attribute, value, attempts, wait_seconds):
        if getattr(self, object_attribute) == value:
            return

        for i in range(0, attempts):
            volume_value = _get_volume_json(self._config, self.id)[request_attribute]
            if volume_value == value:
                setattr(self, object_attribute, volume_value)
                return

            time.sleep(wait_seconds)

        raise HetznerWaitAttemptsExceededException()

    def wait_until_status_is(self, status, attempts=20, wait_seconds=1):
        self._wait_until_attribute_is("status", "status", status, attempts, wait_seconds)

    def wait_until_server_is(self, server_id, attempts=20, wait_seconds=1):
        self._wait_until_attribute_is("server_id", "server", server_id, attempts, wait_seconds)

    @staticmethod
    def _load_from_json(config, json):
        volume = HetznerCloudVolume(config)

        volume.id = int(json["id"])
        volume.created = json["created"]
        volume.name = json["name"]
        volume.server_id = json["server"] if json["server"] is not None else 0
        volume.location = HetznerCloudLocation._load_from_json(json["location"])
        volume.size = json["size"]
        volume.linux_device = json["linux_device"]
        volume.status = json["status"]
        volume.format = json["format"] if json["format"] is not None else ""

        return volume
