import time

from .actions import HetznerCloudAction
from .constants import RESCUE_TYPE_LINUX, RESCUE_TYPE_FREEBSD, BACKUP_WINDOW_2AM_6AM
from .exceptions import HetznerServerNotFoundException, HetznerInvalidArgumentException, HetznerActionException, \
    HetznerWaitAttemptsExceededException
from .shared import _get_results


def _get_server_json(config, server_id):
    status_code, result = _get_results(config, "servers/%s" % server_id)
    if status_code == 404:
        raise HetznerServerNotFoundException()

    return result["server"]


class HetznerCloudServersAction(object):
    """
    This action contains all top-level calls related to servers. Specific server-related calls (such as deleting or
    imaging a server) are done by first retrieving the server (by using the get_all or get methods in this class) and
    then calling the required method on the object returned.

    :Example:
    
        # To delete the server, you first have to retrieve it.
        my_server = client.servers().get(32)

        # And then you can delete it.
        my_server.delete()
    """

    def __init__(self, config):
        """
        Creates a new instance of the HetznerCloudServersAction class.

        :param config: The HetznerCloudConfiguration object, which defines the version of the API the users wish to use.
        """
        self._config = config

    def create(self, name, server_type, image, datacenter=None, start_after_create=True, ssh_keys=[], user_data=None):
        """
        Creates a new server in the Hetzner Cloud.

        :param name: The name of the server.
        :param server_type: The size of the server (i.e. VPS-1, VPS-2).
        :param datacenter: The datacenter to create the server in.
        :param start_after_create: Whether to start the server after it is created (defaults to True).
        :param image: The image to create the server from.
        :param ssh_keys: An array of SSH key names to apply to the server.
        :param user_data: Cloud-Init user data
        :return: A HetznerCloudServer object, that has more options that can modify the server.
        """
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

        _, result = _get_results(self._config, "servers", body=create_params, method="POST")
        if result is None or ("error" in result and result["error"] is not None):
            raise HetznerActionException(result["error"] if result is not None else None)

        return HetznerCloudServer._load_from_json(self._config, result["server"], result["root_password"]), \
               HetznerCloudAction._load_from_json(self._config, result["action"])

    def get(self, server_id):
        """
        Gets a server by its defined id.

        :param server_id: The server's id.
        :return: A server object if the server exists, or a HetznerServerNotFoundException.
        """
        if not isinstance(server_id, int) or server_id == 0:
            raise HetznerServerNotFoundException()

        return HetznerCloudServer._load_from_json(self._config, _get_server_json(self._config, server_id))

    def get_all(self, name=None):
        """
        Retrieves all of the servers associated with the API key's project, but also allows you to filter by name.
        Leaving the "name" parameter as None (or empty) will result in all servers associated with the API key's project
        being brought back.

        Note: Wildcards are NOT currently supported (by this SDK or the API).

        :param name: The name to filter the servers by.
        :return: An array of server objects.
        :rtype: HetznerCloudServer[]
        """
        status_code, results = _get_results(self._config, "servers", {"name": name} if name is not None else None)
        for result in results["servers"]:
            yield HetznerCloudServer._load_from_json(self._config, result)


class HetznerCloudServer(object):
    """
    Represents a cloud server that has been created.
    """

    def __init__(self, config):
        self._config = config
        self.id = 0
        self.name = ""
        self.status = ""
        self.created = None
        self.public_net_ipv4 = ""
        self.public_net_ipv6 = ""
        self.server_type_id = 0
        self.datacenter_id = 0
        self.image_id = 0
        self.iso_id = 0
        self.rescue_enabled = False
        self.locked = False
        self.backup_window = ""
        self.outgoing_traffic = 0
        self.ingoing_traffic = 0
        self.included_traffic = 0
        self.root_password = ""

    def attach_iso(self, iso):
        pass

    def change_name(self, new_name):
        """
        Changes the name of the server to a new, DNS compliant name.

        :param new_name: The string that the server should be renamed to. NOTE: This value should be DNS compliant.
        """
        if not new_name:
            raise HetznerInvalidArgumentException("new_name")

        body = { "name": new_name }
        status_code, result = _get_results(self._config, "servers/%s" % self.id, method="PUT", body=body)
        if status_code != 200:
            raise HetznerActionException()

        self.name = new_name

    def change_reverse_dns_entry(self):
        pass

    def change_type(self):
        pass

    def delete(self):
        """
        Deletes the server, making it immediately unavailable for any further use.

        :return: The action related to the deletion of the server.
        """
        status_code, result = _get_results(self._config, "servers/%s" % self.id, method="DELETE")
        if status_code != 200:
            raise HetznerActionException()

        return HetznerCloudAction._load_from_json(self._config, result["action"])

    def detach_iso(self):
        pass

    def disable_rescue_mode(self):
        """
        Disables rescue mode for the current server.

        :return: The action related to the disabling of rescue mode for the current server.
        """
        status_code, result = _get_results(self._config, "servers/%s/actions/disable_rescue" % self.id, method="POST")
        if status_code != 201:
            raise HetznerActionException()

        self.rescue_enabled = False

        return HetznerCloudAction._load_from_json(self._config, result["action"])

    def enable_backups(self, backup_window=BACKUP_WINDOW_2AM_6AM):
        """
        Enables backups for the current server.

        :param backup_window: The backup window defined in the following format: HH-HH (i.e. 02-04).
        :return: The action related to the enabling of the backups for the current server.
        """
        body = { "backup_window": backup_window }
        status_code, result = _get_results(self._config, "servers/%s/actions/enable_backup" % self.id, method="POST",
                                           body=body)
        if status_code != 201:
            raise HetznerActionException("Invalid backup window choice" if status_code == 422 else None)

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
        body = { "type": rescue_type }
        if ssh_keys and len(ssh_keys > 0) and rescue_type != RESCUE_TYPE_FREEBSD:
            body["ssh_keys"] = ssh_keys

        status_code, result = _get_results(self._config, "servers/%s/actions/enable_rescue" % self.id, method="POST",
                                           body=body)
        if status_code != 201:
            raise HetznerActionException()

        self.rescue_enabled = True

        return result["root_password"], HetznerCloudAction._load_from_json(self._config, result["action"])

    def image(self, description=None, image_type="snapshot"):
        pass

    def power_on(self):
        pass

    def power_off(self):
        pass

    def soft_reboot(self):
        pass

    def rebuild_from_image(self):
        pass

    def reset(self):
        pass

    def reset_root_password(self):
        pass

    def shutdown(self):
        pass

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
        cloud_server.server_type_id = int(json["server_type"]["id"])
        cloud_server.datacenter_id = int(json["datacenter"]["id"] if json["datacenter"] is not None else 0)
        cloud_server.image_id = int(json["image"]["id"] if json["image"] is not None else 0)
        cloud_server.iso_id = int(json["iso"]["id"] if json["iso"] is not None else 0)
        cloud_server.rescue_enabled = bool(json["rescue_enabled"])
        cloud_server.locked = bool(json["locked"])
        cloud_server.backup_window = json["backup_window"]
        cloud_server.outgoing_traffic = int(json["outgoing_traffic"])
        cloud_server.ingoing_traffic = int(json["ingoing_traffic"])
        cloud_server.included_traffic = int(json["included_traffic"])
        cloud_server.root_password = root_password

        return cloud_server

