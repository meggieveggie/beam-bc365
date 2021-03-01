from __future__ import division, print_function

import datetime
import unittest

from nose.tools import assert_equal

from beam_bc365.io.bc_service_api import ServiceConfiguration

class BCServiceAPITest(unittest.TestCase):

    service_config = ServiceConfiguration(
        service="testservice",
        companies=['Cronos'],
        instance='Sandbox',
        username='foo',
        service_key='api_key',
        instance_id='123456789',
        base_url="example.com"
    )

    def test_service_configuration_urls(self):
        expected = ["example.com/123456789/Sandbox/Company('Cronos')/testservice"]
        assert_equal(
            self.service_config.urls,
            expected,
            'expected: {}, got: {}'.format(
                expected,
                self.service_config.urls
                )
        )

    def test_service_configuration_auth_username(self):
        expected_username = "foo"
        assert_equal(
            self.service_config.auth.usernamme,
            expected_username,
            'expected: {}, got: {}'.format(
                expected_username,
                self.service_config.auth.username
                )
        )

    def test_service_configuration_auth_password(self):
        expected_password = "api_key"
        assert_equal(
            self.service_config.auth.password,
            expected_password,
            'expected: {}, got: {}'.format(
                expected_password,
                self.service_config.auth.password
                )
        )
