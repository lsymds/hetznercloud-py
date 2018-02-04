class HetznerConfigurationException(Exception):
    """
    HetznerConfigurationException is an exception that is raised whenever validation on the CloudConfiguration object
    fails.
    """

    def __init__(self, reason):
        super().__init__("Your Hetzner Cloud configuration is incorrect: %s" % reason)


class HetznerServerNotFoundException(Exception):
    """
    HetznerServerNotFoundException is an exception that is raised when a server, requested by the user, cannot be found.
    """
    pass


class HetznerAuthenticationException(Exception):
    """
    HetznerAuthenticationException is an authentication that is raised when authentication fails for a request.
    """

    def __init__(self):
        super().__init__("Authenticated failed. Is your API key correct?")


class HetznerInternalServerErrorException(Exception):
    """
    HetznerInternalServerErrorException is an exception that is thrown whenever the Hetzner API is unavailable (for one
    reason or another). Should this keep occurring, please raise an issue on the Github project where we will raise
    a support issue with the Hetzner API team to get a better error code returned.
    """

    def __init__(self, hetzner_message):
        super().__init__("The Hetzner Cloud API is currently unavailable: %s" % hetzner_message)


class HetznerInvalidArgumentException(Exception):
    """
    HetznerInvalidArgumentException is a generic error message thrown when an argument passed to one of the action
    methods is invalid.
    """

    def __init__(self, argument, message=None):
        if message is not None:
            super().__init__("An invalid argument was (or was not) entered: %s, %s." % (argument, message))
        else:
            super().__init__("An invalid argument was (or was not) entered: %s." % argument)


class HetznerActionException(Exception):
    """
    HetznerActionException is an exception that is raised whenever an action of something fails.
    """

    def __init__(self, error_code):
        if error_code is not None:
            super().__init__("Failed to perform the requested action: %s" % error_code)


class HetznerWaitAttemptsExceededException(Exception):
    """
    HetznerWaitAttemptsExceededException is an exception that is raised when the amount of wait attempts on a wait
    function is exceeded.
    """