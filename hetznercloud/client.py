from .exceptions import HetznerConfigurationException
from .servers import HetznerCloudServersAction


class HetznerCloudClientConfiguration(object):
    """
    This class defines the configuration options available for the Hetzner cloud API. We respect semantic versioning,
    so breaking changes in this file will never be introduced unless the major version increases.
    """

    def __init__(self):
        """
        Initialises the default instance of the configuration object. Validation will not be performed until this
        class is loaded into the cloud client class.
        """
        self.api_key = ""
        self.api_version = 1

    def with_api_key(self, key):
        """
        Modifies the API key associated with this configuration object.

        :param key: The API key to assign to this configuration object.
        :return: The current instance of the cloud configuration object to allow fluent chaining.
        """
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
    """
    Entry point into the Hetzner Cloud SDK. All parts of the cloud SDK are accessible from within this file, though
    other actions (such as server related actions) may be delegated to other objects.
    """

    def __init__(self, configuration):
        """
        Initialises a new instance of the Hetzner Cloud client with a specific configuation. Validation is performed at
        this point, so you may receive an exception of type ConfigurationException if anything is wrong.

        :param configuration:
        """
        if not isinstance(configuration, HetznerCloudClientConfiguration):
            raise HetznerConfigurationException("Invalid configuration type.")

        if not configuration.api_key:
            raise HetznerConfigurationException("Invalid API key.")

        if not isinstance(configuration.api_version, int) or configuration.api_version != 1:
            raise HetznerConfigurationException("The requested API version is not yet supported.")

        self.configuration = configuration

    def actions(self):
        pass

    def datacentres(self):
        pass

    def floating_ips(self):
        pass

    def images(self):
        pass

    def isos(self):
        pass

    def locations(self):
        pass

    def metrics(self):
        pass

    def server_types(self):
        pass

    def servers(self):
        """
        Returns an action object that contains all functionality relevant to servers within the Hetzner Cloud.

        :return: An action object related to servers
        """
        return HetznerCloudServersAction(self.configuration)

    def ssh_keys(self):
        pass
