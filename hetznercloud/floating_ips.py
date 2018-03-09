from hetznercloud.actions import HetznerCloudAction
from .exceptions import HetznerInvalidArgumentException, HetznerActionException
from .shared import _get_results


class HetznerCloudFloatingIpAction(object):
    def __init__(self, config):
        self._config = config

    def create(self, type, home_location=None, server=None, description=None):
        if home_location is None and server is None:
            raise HetznerInvalidArgumentException("home_location_id and server")

        body = {"type": type}
        if home_location is not None:
            body["home_location"] = home_location
        if server is not None:
            body["server"] = server
        if description is not None:
            body["description"] = description

        status_code, results = _get_results(self._config, "floating_ips", method="POST", body=body)
        if status_code != 201:
            raise HetznerActionException(results)

        return HetznerCloudFloatingIp._load_from_json(self._config, results["floating_ip"])

    def get_all(self):
        status_code, results = _get_results(self._config, "floating_ips")
        if status_code != 200:
            raise HetznerActionException(results)

        for result in results["floating_ips"]:
            yield HetznerCloudFloatingIp._load_from_json(self._config, result)

    def get(self, id):
        status_code, result = _get_results(self._config, "floating_ips/%s" % id)
        if status_code != 200:
            raise HetznerActionException(result)

        return HetznerCloudFloatingIp._load_from_json(self._config, result["floating_ip"])


class HetznerCloudFloatingIp(object):
    def __init__(self, config):
        self._config = config
        self.id = 0
        self.description = ""
        self.type = ""
        self.server = 0
        self.ptr_ips = []
        self.ptr_dns_ptrs = []
        self.location_id = 0
        self.blocked = False

    def assign_to_server(self, server_id):
        if not server_id:
            raise HetznerInvalidArgumentException("server_id")

        status_code, result = _get_results(self._config, "floating_ips/%s/actions/assign" % self.id, method="POST",
                                           body={"server": server_id})
        if status_code != 201:
            raise HetznerActionException(result)

        self.server = server_id

        return HetznerCloudAction._load_from_json(self._config, result["action"])

    def change_description(self, new_description):
        status_code, result = _get_results(self._config, "floating_ips/%s" % self.id, method="PUT",
                                           body={"description": new_description})
        if status_code != 200:
            raise HetznerActionException(result)

        self.description = new_description

    def change_reverse_dns_entry(self, ip, dns_ptr=None):
        if not ip:
            raise HetznerInvalidArgumentException("ip")

        status_code, result = _get_results(self._config, "floating_ips/%s/actions/change_dns_ptr" % self.id,
                                           method="POST", body={"ip": ip, "dns_ptr": dns_ptr})
        if status_code != 201:
            raise HetznerActionException(result)

        self.ptr_ips = [ip]
        self.ptr_dns_ptrs = [dns_ptr]

        return HetznerCloudAction._load_from_json(self._config, result["action"])

    def delete(self):
        status_code, result = _get_results(self._config, "floating_ips/%s" % self.id, method="DELETE")
        if status_code != 204:
            raise HetznerActionException(result)

    def unassign_from_server(self):
        status_code, result = _get_results(self._config, "floating_ips/%s/actions/unassign" % self.id, method="POST")
        if status_code != 201:
            raise HetznerActionException(result)

        self.server = 0

        return HetznerCloudAction._load_from_json(self._config, result["action"])

    @staticmethod
    def _load_from_json(config, json):
        float_ip = HetznerCloudFloatingIp(config)

        float_ip.id = int(json["id"])
        float_ip.description = json["description"]
        float_ip.type = json["type"]
        float_ip.server = int(json["server"]) if json["server"] is not None else 0
        float_ip.ptr_ips = [entry["ip"] for entry in json["dns_ptr"]]
        float_ip.ptr_dns_ptrs = [entry["dns_ptr"] for entry in json["dns_ptr"]]
        float_ip.location_id = int(json["home_location"]["id"])
        float_ip.blocked = bool(json["blocked"])

        return float_ip
