class HetznerConfigurationException(Exception):
    """
    ConfigurationException is an exception that is raised whenever validation on the CloudConfiguration object fails.
    """

    def __init__(self, reason):
        super().__init__("Your Hetzner Cloud configuration is incorrect: %s" % reason)