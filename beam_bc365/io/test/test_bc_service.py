from __future__ import division, print_function

import datetime
import unittest
import responses

from nose.tools import assert_equal
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

from beam_bc365.io.bc_service_api import ServiceConfiguration, BusinessCentralSource
from beam_bc365.io import bc_service
import responses

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

class TestReadFromService(unittest.TestCase):

    @responses.activate
    def test_running_pipeline(self):
        responses.add(
            responses.GET,
            "https://example.com/123456/Sandbox/ODataV4/Company('Cronos')/TimeSheetData",
            json=MOCK_BC365,
            status=200
        )
        service_config = ServiceConfiguration(
            service="TimeSheetData",
            companies=['Cronos'],
            instance='Sandbox',
            username='foo',
            service_key='api_key',
            instance_id='123456',
            base_url="https://example.com"
        )
        def _check_input(record):
            assert_equal(
               "TS00001",
               record.get("TimeSheetNo"),
               'expected: {}, got: {}'.format(
                   "TS00001",
                   record.get("TimeSheetNo")
            )
           )
        with beam.Pipeline(options=PipelineOptions()) as p:
            records = p | "Reading records from service" >>  bc_service.ReadFromService(
                    service_config=service_config,
                )
            records | 'Writing to stdout' >> beam.Map(_check_input)
