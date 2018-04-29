import time

from .actions import HetznerCloudAction
from .constants import RESCUE_TYPE_LINUX, RESCUE_TYPE_FREEBSD, BACKUP_WINDOW_2AM_6AM, SERVER_STATUS_RUNNING, \
    SERVER_STATUS_OFF
from .exceptions import HetznerServerNotFoundException, HetznerInvalidArgumentException, HetznerActionException, \
    HetznerWaitAttemptsExceededException
from .shared import _get_results


def _get_server_json(config, server_id):
    status_code, result = _get_results(config, "servers/%s" % server_id)
    if status_code == 404:
        raise HetznerServerNotFoundException()

    if not "server" in result:
        raise HetznerActionException(result)

    return result["server"]


class HetznerCloudServersAction(object):
    def __init__(self, config):
        self._config = config

    def create(self, name, server_type, image, datacenter=None, start_after_create=True, ssh_keys=[], user_data=None):
        if not name or not server_type or not image:
            raise HetznerInvalidArgumentException("name" if not name
                                                  else "server_type" if not server_type
            else "image" if not image
            else "")

        create_params = {
            "name": name,
            "server_type": server_type,
            "image": image,
            "start_after_create": start_after_create
        }

        if datacenter is not None:
            create_params["datacenter"] = datacenter
        if ssh_keys is not None and len(ssh_keys) > 0:
            create_params["ssh_keys"] = ssh_keys
        if user_data is not None:
            create_params["user_data"] = user_data

        status_code, result = _get_results(self._config, "servers", body=create_params, method="POST")
        if status_code != 201 or result is None or ("error" in result and result["error"] is not None):
            raise HetznerActionException(result)

        return HetznerCloudServer._load_from_json(self._config, result["server"], result["root_password"]), \
               HetznerCloudAction._load_from_json(self._config, result["action"])

    def get(self, server_id):
        if not isinstance(server_id, int) or server_id == 0:
            raise HetznerServerNotFoundException()

        return HetznerCloudServer._load_from_json(self._config, _get_server_json(self._config, server_id))

    def get_all(self, name=None):
        status_code, results = _get_results(self._config, "servers", {"name": name} if name is not None else None)
        if status_code != 200:
            raise HetznerActionException(results)
        
        for result in results["servers"]:
            yield HetznerCloudServer._load_from_json(self._config, result)


class HetznerCloudServer(object):
    def __init__(self, config):
        self._config = config
        self.id = 0
        self.name = ""
        self.status = ""
        self.created = None
        self.public_net_ipv4 = ""
        self.public_net_ipv6 = ""
        self.server_type = ""
        self.datacenter_id = 0
        self.image_id = ""
        self.iso = ""
        self.rescue_enabled = False
        self.locked = False
        self.backup_window = ""
        self.outgoing_traffic = 0
        self.ingoing_traffic = 0
        self.included_traffic = 0
        self.root_password = ""

    def attach_iso(self, iso):
        if not iso:
            raise HetznerInvalidArgumentException("iso")

        status_code, result = _get_results(self._config, "servers/%s/actions/attach_iso" % self.id, method="POST",
                                           body={"iso": iso})
        if status_code != 201:
            raise HetznerActionException(result)

        self.iso = iso

        return HetznerCloudAction._load_from_json(self._config, result["action"])

    def change_name(self, new_name):
        if not new_name:
            raise HetznerInvalidArgumentException("new_name")

        body = {"name": new_name}
        status_code, result = _get_results(self._config, "servers/%s" % self.id, method="PUT", body=body)
        if status_code != 200:
            raise HetznerActionException(result)

        self.name = new_name

    def change_reverse_dns_entry(self, ip, dns_pointer=None):
        if not ip:
            raise HetznerInvalidArgumentException("ip")

        status_code, result = _get_results(self._config, "servers/%s/actions/change_dns_ptr" % self.id, method="POST",
                                           body={"ip": ip, "dns_ptr": dns_pointer})
        if status_code != 201:
            raise HetznerActionException(result)

        return HetznerCloudAction._load_from_json(self._config, result["action"])

    def change_type(self, new_instance_type, upgrade_disk=True):
        if not new_instance_type:
            raise HetznerInvalidArgumentException("new_instance_type")

        status_code, result = _get_results(self._config, "servers/%s/actions/change_type" % self.id, method="POST",
                                           body={"server_type": new_instance_type, "upgrade_disk": upgrade_disk})
        if status_code != 201:
            raise HetznerActionException(result)

        self.server_type = new_instance_type

        return HetznerCloudAction._load_from_json(self._config, result["action"])

    def delete(self):
        status_code, result = _get_results(self._config, "servers/%s" % self.id, method="DELETE")
        if status_code != 200:
            raise HetznerActionException(result)

        self.iso = ""

        return HetznerCloudAction._load_from_json(self._config, result["action"])

    def detach_iso(self):
        status_code, result = _get_results(self._config, "servers/%s/actions/detach_iso", method="POST")
        if status_code != 201:
            return HetznerActionException(result)

        return HetznerCloudAction._load_from_json(self._config, result["action"])

    def disable_rescue_mode(self):
        status_code, result = _get_results(self._config, "servers/%s/actions/disable_rescue" % self.id, method="POST")
        if status_code != 201:
            raise HetznerActionException(result)

        self.rescue_enabled = False

        return HetznerCloudAction._load_from_json(self._config, result["action"])

    def enable_backups(self, backup_window=BACKUP_WINDOW_2AM_6AM):
        status_code, result = _get_results(self._config, "servers/%s/actions/enable_backup" % self.id, method="POST",
                                           body={"backup_window": backup_window})
        if status_code != 201:
            raise HetznerActionException("Invalid backup window choice" if status_code == 422 else result)

        self.backup_window = backup_window

        return HetznerCloudAction._load_from_json(self._config, result["action"])

    def enable_rescue_mode(self, rescue_type=RESCUE_TYPE_LINUX, ssh_keys=[]):
        """
        Enables rescue mode for the current server.

        NOTE: This will not reboot your server, you will need to do this either through the console or by calling the
              shutdown method.

        NOTE: Adding SSH keys to the rescue mode is only supported for RESCUE_TYPE_LINUX and RESCUE_TYPE_LINUX32.
              Attempting to pass an SSH key with another rescue type will result in it being ignored, and you having
              to log in with a root password.

        :param rescue_type: The rescue image to use.
        :param ssh_keys: An array of SSH key ids to load into the rescue mode (if it is linux based)
        :return: A tuple containing the root SSH password to access the recovery mode and the action to track the
                 progress of the request.
        """
        body = {"type": rescue_type}
        if ssh_keys and len(ssh_keys > 0) and rescue_type != RESCUE_TYPE_FREEBSD:
            body["ssh_keys"] = ssh_keys

        status_code, result = _get_results(self._config, "servers/%s/actions/enable_rescue" % self.id, method="POST",
                                           body=body)
        if status_code != 201:
            raise HetznerActionException(result)

        self.rescue_enabled = True

        return result["root_password"], HetznerCloudAction._load_from_json(self._config, result["action"])

    def image(self, description=None, image_type="snapshot"):
        body = {"type": image_type}
        if description is not None:
            body["description"] = description

        status_code, result = _get_results(self._config, "servers/%s/actions/create_image" % self.id, method="POST",
                                           body=body)
        if status_code != 201:
            raise HetznerActionException(result)

        return result["image"]["id"], HetznerCloudAction._load_from_json(self._config, result["action"])

    def power_on(self):
        status_code, result = _get_results(self._config, "servers/%s/actions/poweron" % self.id, method="POST")
        if status_code != 201:
            raise HetznerActionException(result)

        self.status = SERVER_STATUS_RUNNING

        return HetznerCloudAction._load_from_json(self._config, result["action"])

    def power_off(self):
        status_code, result = _get_results(self._config, "servers/%s/actions/poweroff" % self.id, method="POST")
        if status_code != 201:
            raise HetznerActionException(result)

        self.status = SERVER_STATUS_OFF

        return HetznerCloudAction._load_from_json(self._config, result["action"])

    def soft_reboot(self):
        status_code, result = _get_results(self._config, "servers/%s/actions/reboot" % self.id, method="POST")
        if status_code != 201:
            raise HetznerActionException(result)

        return HetznerCloudAction._load_from_json(self._config, result["action"])

    def rebuild_from_image(self, image):
        if not image:
            raise HetznerInvalidArgumentException("image")

        status_code, result = _get_results(self._config, "servers/%s/actions/rebuild" % self.id, method="POST",
                                           body={"image": image})
        if status_code != 201:
            raise HetznerActionException(result)

        self.image_id = image

        return HetznerCloudAction._load_from_json(self._config, result["action"])

    def reset(self):
        status_code, result = _get_results(self._config, "servers/%s/actions/reset" % self.id, method="POST")
        if status_code != 201:
            raise HetznerActionException(result)

        return HetznerCloudAction._load_from_json(self._config, result["action"])

    def reset_root_password(self):
        status_code, result = _get_results(self._config, "servers/%s/actions/reset_password" % self.id, method="POST")
        if status_code != 201:
            raise HetznerActionException(result)

        return result["root_password"], HetznerCloudAction._load_from_json(self._config, result["action"])

    def shutdown(self):
        status_code, result = _get_results(self._config, "servers/%s/actions/shutdown" % self.id, method="POST")
        if status_code != 201:
            raise HetznerActionException(result)

        return HetznerCloudAction._load_from_json(self._config, result["action"])

    def wait_until_status_is(self, status, attempts=20, wait_seconds=1):
        """
        Sleeps the executing thread (a second each loop) until the status is either what the user requires or the
        attempt count is exceeded, in which case an exception is thrown.

        :param status: The status the action needs to be.
        :param attempts: The number of attempts to query the action's status.
        :param wait_seconds: The number of seconds to wait for between each attempt.
        :return: An exception, unless the status matches the status parameter.
        """
        if self.status == status:
            return

        for i in range(0, attempts):
            server_status = _get_server_json(self._config, self.id)["status"]
            if server_status == status:
                self.status = server_status
                return

            time.sleep(wait_seconds)

        raise HetznerWaitAttemptsExceededException()

    @staticmethod
    def _load_from_json(config, json, root_password=None):
        cloud_server = HetznerCloudServer(config)

        cloud_server.id = json["id"]
        cloud_server.name = json["name"]
        cloud_server.status = json["status"]
        cloud_server.created = json["created"]
        cloud_server.public_net_ipv4 = json["public_net"]["ipv4"]["ip"]
        cloud_server.public_net_ipv6 = json["public_net"]["ipv6"]["ip"]
        cloud_server.server_type = json["server_type"]["name"]
        cloud_server.datacenter_id = int(json["datacenter"]["id"] if json["datacenter"] is not None else 0)
        cloud_server.image_id = json["image"]["name"] if json["image"] is not None else ""
        cloud_server.iso_id = json["iso"]["name"] if json["iso"] is not None else ""
        cloud_server.rescue_enabled = bool(json["rescue_enabled"])
        cloud_server.locked = bool(json["locked"])
        cloud_server.backup_window = json["backup_window"]
        cloud_server.outgoing_traffic = int(json["outgoing_traffic"])
        cloud_server.ingoing_traffic = int(json["ingoing_traffic"])
        cloud_server.included_traffic = int(json["included_traffic"])
        cloud_server.root_password = root_password

        return cloud_server
