import logging
from .base_session import BaseSession
from .exceptions import raise_requests_error

log = logging.getLogger(__name__)


class AgentSession(BaseSession):
    """Methods for agents."""
    def __init__(self, cache_methods=None, *args, **kwargs):
        cache_methods = cache_methods or ['get_agent']
        super(AgentSession, self).__init__(cache_methods=cache_methods, *args, **kwargs)

    def get_agent(self, client_id):
        """Get agents.

        Args:
            client_id: client id for which to get agents

        Returns:
            list: agents
        """
        if isinstance(client_id, int):
            log.warning('deprecated: client_id support for int for backward compatibility only')
            client_id = str(client_id)
        path = 'Agent'
        qstr_vals = {
            'clientId': client_id
        }
        try:
            res = self.request('GET', path, qstr_vals=qstr_vals)
            data = res.json().get('agentProperties')
        except Exception as e:
            msg = f'Fail to  get agents for client {client_id} - {str(e)}'
            raise_requests_error(500, msg)

        if not data:
            msg = f'No agents found for client {client_id}'
            raise_requests_error(404, msg)

        return data

