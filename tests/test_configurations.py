from __future__ import absolute_import
import unittest

from hetznercloud import HetznerCloudClientConfiguration, HetznerCloudClient, HetznerConfigurationException


class TestConfigurations(unittest.TestCase):
    def test_invalid_instance_of_configuration_results_in_an_exception(self):
        try:
            HetznerCloudClient(1231232)
            self.fail()
        except HetznerConfigurationException:
            pass

    def test_invalid_api_key_results_in_an_exception(self):
        try:
            HetznerCloudClient(HetznerCloudClientConfiguration().with_api_key(None))
            self.fail()
        except HetznerConfigurationException:
            pass

    def test_invalid_api_version_results_in_an_exception(self):
        try:
            HetznerCloudClient(HetznerCloudClientConfiguration().with_api_key("abcdefg").with_api_version(2))
            self.fail()
        except HetznerConfigurationException:
            pass