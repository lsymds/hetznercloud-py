from os import environ

from hetznercloud import HetznerCloudClientConfiguration

valid_configuration = HetznerCloudClientConfiguration().with_api_key(environ.get("HNER_API_KEY")).with_api_version(1)
