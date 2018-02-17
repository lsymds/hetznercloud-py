import time

from .constants import ACTION_STATUS_ERROR
from .exceptions import HetznerWaitAttemptsExceededException, HetznerInternalServerErrorException
from .shared import _get_results


def _get_action_json(config, id):
    status_code, json = _get_results(config, "actions/%s" % id)
    return json["action"]

class HetznerCloudActionsAction(object):
    pass

class HetznerCloudAction(object):
    """
    When actions in the API (such as creating a server) are performed, the API will naturally not wait until the request
    finishes its requested action (as these things can sometimes take a long time).

    Instead, the cloud API returns an 'action', which can be used to check up on the status of specific tasks.
    """
    def __init__(self, config):
        self.config = config
        self.id = 0
        self.command = ""
        self.status = ""
        self.progress = 0
        self.started = ""
        self.finished = ""
        self.error = { "code": "", "message": "" }

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
            action_status = _get_action_json(self.config, self.id)
            if action_status["status"] == status:
                self.status = action_status
                return

            if action_status["status"] == ACTION_STATUS_ERROR:
                raise HetznerInternalServerErrorException(action_status["error"])

            time.sleep(wait_seconds)

        raise HetznerWaitAttemptsExceededException()

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