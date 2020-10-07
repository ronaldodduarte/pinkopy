import logging

from .base_session import BaseSession
from .exceptions import raise_requests_error
from requests import HTTPError

log = logging.getLogger(__name__)


class SubclientSession(BaseSession):
    """Methods for subclients."""
    def __init__(self, cache_methods=None, *args, **kwargs):
        cache_methods = cache_methods or ['get_subclients',
                                          'get_subclient_properties',
                                          'get_suclient_bkp_info_by_client_id']
        super(SubclientSession, self).__init__(cache_methods=cache_methods, *args, **kwargs)

    def get_subclients(self, client_id):
        """Get subclients.

        Args:
            client_id: client id for which to get subclients

        Returns:
            list: subclients
        """
        if isinstance(client_id, int):
            log.warning('deprecated: client_id support for int for backward compatibility only')
            client_id = str(client_id)
        path = 'Subclient'
        qstr_vals = {
            'clientId': client_id
        }
        try:
            res = self.request('GET', path, qstr_vals=qstr_vals)
            data = res.json()
            subclients = data.get('subClientProperties')
        except Exception as e:
            msg = f'Fail to  get subclients for client {client_id} - {str(e)}'
            raise_requests_error(500, msg)

        if not subclients:
            msg = 'No subclients for client {}'.format(client_id)
            raise_requests_error(404, msg)
        return subclients

    def get_subclient_properties(self, subclient_id):
        """Get subclient properties.

        Args:
            subclient_id: subclient id for which to get subclient properties

        Returns:
            Dict: subclient properties
        """
        subclient_id = str(subclient_id)
        path = 'Subclient/' + subclient_id
        try:
            res = self.request('GET', path)
            data = res.json()
        except HTTPError as e:
            if e.response.status_code == 404:
                msg = f'Subclient {subclient_id} not found.'
                raise_requests_error(404, msg)
            else:
                raise_requests_error(e.response.status_code, str(e))
        except Exception as e:
            raise_requests_error(500, str(e))

        subclient_properties = data.get('subClientProperties')
        if not subclient_properties:
            msg = 'No subclient properties for subclient_id {}'.format(subclient_id)
            raise_requests_error(404, msg)
        return subclient_properties

    def get_suclient_bkp_info_by_client_id(self, client_id):
        try:
            subclients_info = self.get_subclients(client_id)
        except Exception as e:
            raise e

        subclients_bkp_details = list()
        for subclient in subclients_info:
            subclient_id = subclient['subClientEntity']['subclientId']
            try:
                subclient_bkp_info = self.get_subclient_properties(subclient_id)
            except Exception as e:
                subclient_bkp_info = [{'error': e.args[0]}]

            subclients_bkp_details.append(subclient_bkp_info)

        return subclients_bkp_details
