import json

import requests

from .exceptions import HetznerAuthenticationException, HetznerInternalServerErrorException, HetznerActionException, HetznerRateLimitExceeded


def _get_results(config, endpoint, url_params=None, body=None, method="GET"):
    api = "https://api.hetzner.cloud/v%s/%s?" % (config.api_version, endpoint)
    headers = {"Authorization": "Bearer %s" % config.api_key}
    data = json.dumps(body) if body is not None else None

    if method == "GET":
        request = requests.get(api, headers=headers, params=url_params)
    elif method == "POST" or (method == "GET" and body is not None):
        request = requests.post(api, data=data, headers=headers, params=url_params)
    elif method == "DELETE":
        request = requests.delete(api, headers=headers)
    elif method == "PUT":
        request = requests.put(api, headers=headers, data=data)

    if request.status_code == 401 or request.status_code == 403:
        raise HetznerAuthenticationException()

    if request.status_code == 429:
        raise HetznerRateLimitExceeded()

    if request.status_code == 500:
        raise HetznerInternalServerErrorException(request.text)

    if not request.text:
        return request.status_code, ""

    js = request.json()
    if "action" in js and "error" in js["action"] and js["action"]["error"] is not None:
        raise HetznerActionException(js["action"]["error"])

    return request.status_code, js
