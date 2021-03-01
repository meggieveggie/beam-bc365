from __future__ import division, print_function

import urllib

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
        self.urls = self._get_urls(
            service=service,
            companies=companies,
            instance=instance,
            instance_id=instance_id,
            base_url=base_url
        )
        self.auth = HTTPBasicAuth(username, service_key)

    @staticmethod
    def _get_urls(service,companies,instance,instance_id,base_url):
        urls = []
        for company in companies:
            urls.append(
               f"{base_url}/{instance_id}/{instance}/Company('{urllib.parse.quote(company)}')/{service}"
            )
        return urls
