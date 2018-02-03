class HetznerCloudAction(object):
    """
    When actions in the API (such as creating a server) are performed, the API will naturally not wait until the request
    finishes its requested action (as these things can sometimes take a long time).

    Instead, the cloud API returns an 'action', which can be used to check up on the status of specific tasks.
    """
    def __init__(self, configuration):
        self._configuration = configuration
        self.id = 0
        self.command = ""
        self.status = ""
        self.progress = 0
        self.started = ""
        self.finished = ""
        self.error = { "code": "", "message": "" }

    @staticmethod
    def _load_from_json(configuration, json):
        action = HetznerCloudAction(configuration)

        action.id = json["id"]
        action.command = json["command"]
        action.status = json["status"]
        action.progress = json["progress"]
        action.started = json["started"]
        action.finished = json["finished"]
        action.error = json["error"]

        return action