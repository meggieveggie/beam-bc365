from __future__ import division, print_function

import urllib
import requests

from requests.auth import HTTPBasicAuth


class ServiceConfiguration(object):
    """Holds parameters for accessing a Microsfot Business Central 365.
    User to pass database access parameters to
    :class:`~beam_nuggets.io.relational_db_api.SqlAlchemyDB`.
    ``SourceConfiguration.url`` provides the database url used by SqlAlchemy to
    connect to the database.
    Args:
        username (str): Username for Business Central 365.
        service_key (str): API Key for Business Central 365.
        companies (list): List of Companies to call endpoints for.
        service (str): The service to call.
        instance (str): The Business Central 365 Instance.
        instance_id (str): The Ownership instance if
            found in the Business Central 365 URL.
    """
    def __init__(
        self,
        username,
        service_key,
        companies,
        service,
        instance,
        instance_id,
        base_url="https://api.businesscentral.dynamics.com/v2.0"
    ):
        self.url_data = self._get_urls(
            service=service,
            companies=companies,
            instance=instance,
            instance_id=instance_id,
            base_url=base_url
        )
        self.auth = HTTPBasicAuth(username, service_key)

    @staticmethod
    def _get_urls(service,companies,instance,instance_id,base_url):
        url_data = []
        for company in companies:
            url_data.append({
               'endpoint': f"{base_url}/{instance_id}/{instance}/ODataV4/Company('{urllib.parse.quote(company)}')/{service}",
               'company': company
            })
        return url_data


class BusinessCentralSource(object):

    def __init__(self, service_config):
        self._service_config = service_config

    def read_data(self):
        for endpoint_data in self._service_config.url_data:
            for record in self.service_data(endpoint_data):
                yield record
    
    def service_data(self, endpoint_data):
        headers = {
            "OData-MaxVersion": "4.0",
            "OData-Version": "4.0",
            "Accept": "application/json",
            "Content-Type": "application/json; charset=utf-8",
            "Prefer": "odata.include-annotations=OData.Community.Display.V1.FormattedValue"
        }
        res = requests.get(
            endpoint_data.get('endpoint'),
            auth=self._service_config.auth,
            headers=headers
        )
        for record in res.json().get('value'):
            # Company gets added to records for instances that collect multiple companies
            record['Company'] =  endpoint_data.get('company')
            yield record
