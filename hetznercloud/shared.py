import json

import requests

from .exceptions import HetznerAuthenticationException, HetznerInternalServerErrorException


def _get_results(config, endpoint, url_params=None, body=None, method="GET"):
    api = "https://api.hetzner.cloud/v%s/%s?" % (config.api_version, endpoint)

    headers = {"Authorization": "Bearer %s" % config.api_key}

    if method == "GET":
        request = requests.get(api, headers=headers, params=url_params)
    elif method == "POST" or (method == "GET" and body is not None):
        request = requests.post(api, data=json.dumps(body), headers=headers, params=url_params)
    elif method == "DELETE":
        request = requests.delete(api, headers=headers)

    if request.status_code == 401 or request.status_code == 403:
        raise HetznerAuthenticationException()

    if request.status_code == 500:
        raise HetznerInternalServerErrorException(request.text)

    return request.status_code, request.json()
