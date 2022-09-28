from __future__ import division, print_function

import datetime
import unittest
import responses

from nose.tools import assert_equal

from beam_bc365.io.bc_service_api import ServiceConfiguration, BusinessCentralSource


class BCServiceConfigTest(unittest.TestCase):

    service_config = ServiceConfiguration(
        service="testservice",
        companies=['Cronos'],
        instance='Sandbox',
        tenant_id='123456789',
        base_url="example.com",
        auth_url="example.com",
        client_id="123456",
        client_secret="secret"
    )

    def test_service_configuration_urls(self):
        expected = "example.com/123456789/Sandbox/ODataV4/Company('Cronos')/testservice"
        assert_equal(
            self.service_config.url_data[0].get('endpoint'),
            expected,
            'expected: {}, got: {}'.format(
                expected,
                self.service_config.url_data[0].get('endpoint')
                )
        )

    def test_service_configuration_auth_url(self):
        expected_auth_url = "example.com"
        assert_equal(
            self.service_config.auth_url,
            expected_auth_url,
            'expected: {}, got: {}'.format(
                expected_auth_url,
                self.service_config.auth_url
                )
        )

    def test_service_configuration_tenant_id(self):
        expected_tenant_id = "123456789"
        assert_equal(
            self.service_config.tenant_id,
            expected_tenant_id,
            'expected: {}, got: {}'.format(
                expected_tenant_id,
                self.service_config.tenant_id
                )
        )

    def test_service_configuration_client_id(self):
        expected_client_id = "123456"
        assert_equal(
            self.service_config.client_id,
            expected_client_id,
            'expected: {}, got: {}'.format(
                expected_client_id,
                self.service_config.client_id
                )
        )
    
    def test_service_configuration_client_secret(self):
        expected_client_secret = "secret"
        assert_equal(
            self.service_config.client_secret,
            expected_client_secret,
            'expected: {}, got: {}'.format(
                expected_client_secret,
                self.service_config.client_secret
                )
        )


MOCK_BC365 = {
    '@odata.context': "https://example.com/123456/Sandbox/ODataV4/$metadata#Company('Cronos')/TimeSheetData",
    'value': [
        {
            'TimeSheetNo': 'TS00001',
            'Date': '2021-01-04',
            'JobNo': '10000001',
            'JobTaskNo': '101',
            'Quantity': 8,
            'Status': 'Approved',
            'CreatedAt': '2021-01-14T09:14:10.013Z',
            'UpdatedAt': '2021-02-02T21:14:14.327Z',
            'ResourceNo': 'FOO',
            'OwnerUserID': 'FOO.BAR',
            'AuxiliaryIndex1': 10000,
            'AuxiliaryIndex2': 'TS00001'
        },
        {
            'TimeSheetNo': 'TS00001',
            'Date': '2021-01-05',
            'JobNo': '10000001',
            'JobTaskNo': '102',
            'Quantity': 8,
            'Status': 'Approved',
            'CreatedAt': '2021-01-14T09:14:10.797Z',
            'UpdatedAt': '2021-02-02T21:14:14.707Z',
            'ResourceNo': 'FOO',
            'OwnerUserID': 'FOO.BOO',
            'AuxiliaryIndex1': 10000,
            'AuxiliaryIndex2': 'TS00001'
        }
    ]
}

class BCSourceTest(unittest.TestCase):

    bc_source = BusinessCentralSource(ServiceConfiguration(
        service="TimeSheetData",
        companies=['Cronos'],
        instance='Sandbox',
        tenant_id='123456',
        base_url="https://example.com",
        auth_url="https://auth.com",
        client_id="123456",
        client_secret="secret"
    ))

    @responses.activate
    def test_read_data(self):
        responses.add(
            responses.GET,
            "https://example.com/123456/Sandbox/ODataV4/Company('Cronos')/TimeSheetData",
            json=MOCK_BC365,
            status=200
        )
        responses.add(
            responses.POST,
            "https://auth.com/123456/oauth2/v2.0/token",
            json={
                'access_token': 't'
            },
            status=200
        )
        for record in self.bc_source.read_data():
           assert_equal(
               "TS00001",
               record.get("TimeSheetNo"),
               'expected: {}, got: {}'.format(
                "TS00001",
                 record.get("TimeSheetNo")
            )
           )


