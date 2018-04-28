class HetznerConfigurationException(Exception):
    def __init__(self, reason):
        super(HetznerConfigurationException, self).__init__("Your Hetzner Cloud configuration is incorrect: %s" % reason)


class HetznerServerNotFoundException(Exception):
    pass


class HetznerAuthenticationException(Exception):
    def __init__(self):
        super(HetznerAuthenticationException, self).__init__("Authenticated failed. Is your API key correct?")


class HetznerInternalServerErrorException(Exception):
    def __init__(self, hetzner_message):
        super(HetznerInternalServerErrorException, self).__init__("The Hetzner Cloud API is currently unavailable: %s" % hetzner_message)


class HetznerInvalidArgumentException(Exception):
    def __init__(self, argument, message=None):
        if message is not None:
            super(HetznerInvalidArgumentException, self).__init__("An invalid argument was (or was not) entered: %s, %s." % (argument, message))
        else:
            super(HetznerInvalidArgumentException, self).__init__("An invalid argument was (or was not) entered: %s." % argument)


class HetznerActionException(Exception):
    def __init__(self, error_code=None):
        if error_code is not None:
            super(HetznerActionException, self).__init__("Failed to perform the requested action: %s" % error_code)
        else:
            super(HetznerActionException, self).__init__("Failed to perform the requested action.")


class HetznerWaitAttemptsExceededException(Exception):
    pass