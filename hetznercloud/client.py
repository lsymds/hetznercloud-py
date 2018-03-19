from .floating_ips import HetznerCloudFloatingIpAction
from .ssh_keys import HetznerCloudSSHKeysAction
from .images import HetznerCloudImagesAction
from .datacenters import HetznerCloudDatacentersAction
from .exceptions import HetznerConfigurationException
from .isos import HetznerCloudIsosAction
from .locations import HetznerCloudLocationsAction
from .server_types import HetznerCloudServerTypesAction
from .servers import HetznerCloudServersAction


class HetznerCloudClientConfiguration(object):
    def __init__(self):
        self.api_key = ""
        self.api_version = 1

    def with_api_key(self, key):
        self.api_key = key
        return self

    def with_api_version(self, version):
        """
        Modifies the API version associated with this configuration object. Currently, there is only one API version
        available (1), so using this method to pick a different version will result in a configuration exception being
        raised when this object is passed into the HetznerCloudClient constructor.

        :rtype: object
        :param version: The version of the client to use.
        :return: The current instance of the cloud configuration object to allow fluent chaining.
        """
        self.api_version = version
        return self


class HetznerCloudClient(object):
    def __init__(self, configuration):
        if not isinstance(configuration, HetznerCloudClientConfiguration):
            raise HetznerConfigurationException("Invalid configuration type.")

        if not configuration.api_key:
            raise HetznerConfigurationException("Invalid API key.")

        if not isinstance(configuration.api_version, int) or configuration.api_version != 1:
            raise HetznerConfigurationException("The requested API version is not yet supported.")

        self.configuration = configuration

        # alias for datacentres method
        self.datacenters = self.datacentres

    def datacentres(self):
        return HetznerCloudDatacentersAction(self.configuration)

    def floating_ips(self):
        return HetznerCloudFloatingIpAction(self.configuration)

    def images(self):
        return HetznerCloudImagesAction(self.configuration)

    def isos(self):
        return HetznerCloudIsosAction(self.configuration)

    def locations(self):
        return HetznerCloudLocationsAction(self.configuration)

    def server_types(self):
        return HetznerCloudServerTypesAction(self.configuration)

    def servers(self):
        return HetznerCloudServersAction(self.configuration)

    def ssh_keys(self):
        return HetznerCloudSSHKeysAction(self.configuration)
