import logging
from requests import HTTPError
from .base_session import BaseSession
from .exceptions import raise_requests_error
import re

log = logging.getLogger(__name__)


class ClientSession(BaseSession):
    """Methods for clients."""
    def __init__(self, cache_methods=None, *args, **kwargs):
        cache_methods = cache_methods or ['get_client',
                                          'get_client_properties',
                                          'get_clients',
                                          'get_clients_list'
                                          ]
        super(ClientSession, self).__init__(cache_methods=cache_methods, *args, **kwargs)
        self.clients_list = self._get_clients_list()

    def get_client(self, client_id):
        """Get client.

        Args:
            client_id (str): client id

        Returns:
            dict: client
        """
        if isinstance(client_id, int):
            log.warning('deprecated: client_id support for int for backward compatibility only')
            client_id = str(client_id)
        try:
            try:
                return [c for c in self.get_clients()
                        if str(c['client']['clientEntity']['clientId']) == client_id][0]
            except KeyError:
                # support previous Commvault api versions
                return [c for c in self.get_clients()
                        if str(c['client']['clientEntity']['@clientId']) == client_id][0]
        except IndexError:
            msg = 'Client {} not in client list.'.format(client_id)
            raise_requests_error(404, msg)

    def get_client_properties(self, client_id):
        """Get client properties.

        This call sometimes replies in XML, because who cares about
        Accept headers right. So, we must take the reply in XML and
        convert it to JSON to maintain sanity.

        Args:
            client_id (str): client id

        Returns:
            dict: client properties
        """
        if isinstance(client_id, int):
            log.warning('deprecated: client_id support for int for backward compatibility only')
            client_id = str(client_id)
        path = 'Client/{}'.format(client_id)
        try:
            res = self.request('GET', path)
            data = res.json()
            props = data.get('clientProperties')
        except Exception as e:
            msg = f'Fail to get properties for client {client_id} - {str(e)}'
            raise_requests_error(500, msg)

        if not props:
            msg = f'No client properties found for client {client_id}'
            raise_requests_error(404, msg)
        return props

    def get_clients(self):
        """Get clients.

        Returns:
            list: clients
        """
        path = 'Client'

        try:
            res = self.request('GET', path)
            data = res.json()
            clients = data.get('clientProperties')
        except Exception as e:
            msg = f'Fail to get clients list from Commvault - {str(e)}'
            raise_requests_error(500, msg)

        if not clients:
            msg = 'No clients found in Commvault'
            raise_requests_error(404, msg)

        return clients

    def _get_clients_list(self):
        """Get clients list with specific fields.

        Returns:
            dict: clients
        """

        try:
            clients_ = self.get_clients()
        except HTTPError as e:
            raise_requests_error(404, str(e))
        except Exception as e:
            raise_requests_error(500, str(e))

        client_list = dict()
        for item in clients_:
            client_list[item['client']['clientEntity']['clientName'].lower()] = {
                'hostName': item['client']['clientEntity']['hostName'],
                'clientId': item['client']['clientEntity']['clientId'],
                'displayName': item['client']['clientEntity']['displayName'],
                'clientName': item['client']['clientEntity']['clientName']
            }

        return client_list

    def search_client_by_name(self, host_name):
        client_name = host_name.split('.')[0].lower()
        clients = list(filter(lambda _client: re.search(client_name, _client), list(self.clients_list.keys())))
        clients_list = list()
        for client in clients:
            clients_list.append(self.clients_list.get(client))

        if not clients_list:
            msg = f'No clients found for host {host_name}'
            raise_requests_error(404, msg)

        return clients_list
