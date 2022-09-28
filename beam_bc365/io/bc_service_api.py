from __future__ import division, print_function

import urllib
import requests

from requests.auth import HTTPBasicAuth


class ServiceConfiguration():
    """Holds parameters for accessing a Microsfot Business Central 365.
    User to pass database access parameters to
    :class:`~beam_nuggets.io.relational_db_api.SqlAlchemyDB`.
    ``SourceConfiguration.url`` provides the database url used by SqlAlchemy to
    connect to the database.
    Args:
        companies (list): List of Companies to call endpoints for.
        service (str): The service to call.
        instance (str): The Business Central 365 Instance.
        tenant_id (str): The tenant id of your Azure Active Directory.
        client_id (str): The client id of your AAD OAuth App.
        client_secret(str): The client secret of your AAD OAuth App.
    """
    def __init__(
        self,
        client_id,
        client_secret,
        tenant_id,
        companies,
        service,
        instance,
        base_url="https://api.businesscentral.dynamics.com/v2.0",
        auth_url="https://login.microsoftonline.com",
        scope="https://api.businesscentral.dynamics.com/.default"
    ):
        self.url_data = self._get_urls(
            service=service,
            companies=companies,
            instance=instance,
            tenant_id=tenant_id,
            base_url=base_url
        )
        self.auth_url =  auth_url
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope

        

    @staticmethod
    def _get_urls(service,companies,instance,tenant_id,base_url):
        url_data = []
        for company in companies:
            url_data.append({
               'endpoint': f"{base_url}/{tenant_id}/{instance}/ODataV4/Company('{urllib.parse.quote(company)}')/{service}",
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
        token = ""
        res = requests.post(
            url=f"{self._service_config.auth_url}/{self._service_config.tenant_id}/oauth2/v2.0/token",
            data={
                'grant_type': 'client_credentials',
                'client_id': self._service_config.client_id,
                'client_secret': self._service_config.client_secret,
                'scope': self._service_config.scope
            }
        )
        if res.status_code == 200:
            token = res.json().get("access_token")
        else:
            raise Exception("Failed to get authentication token")
        headers = {
            "OData-MaxVersion": "4.0",
            "OData-Version": "4.0",
            "Accept": "application/json",
            "Content-Type": "application/json; charset=utf-8",
            "Prefer": "odata.include-annotations=OData.Community.Display.V1.FormattedValue",
            "Authorization": f"Bearer {token}"
        }
        url = endpoint_data.get('endpoint')
        has_next = True
        while has_next:
            res = requests.get(
                url,
                headers=headers
            )
            if res.json().get("@odata.nextLink"):
                # Set the pagination link
                url = res.json().get("@odata.nextLink")
            else:
                has_next = False
            for record in res.json().get('value'):
                # Company gets added to records for instances that collect multiple companies
                record['Company'] =  endpoint_data.get('company')
                yield record
