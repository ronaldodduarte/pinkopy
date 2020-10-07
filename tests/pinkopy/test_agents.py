from unittest import TestCase
from unittest.mock import *
from requests import Response, exceptions
import unittest
from pinkopy.agents import *
from pinkopy.agents import AgentSession
from pinkopy.exceptions import raise_requests_error


class TestAgentSession(TestCase):

    def test_get_agent_when_receive_a_request_exception_should_return_status_500(self):
        with patch('pinkopy.base_session.BaseSession.request') as mock_request:
            mock_request.side_effect = Exception('Some Exception')

            self.assertRaises(Exception, AgentSession.get_agent, AgentSession, 'client_id')

    def test_get_agent_when_receive_no_data_should_return_exceptions_HTTPError(self):
        with patch('pinkopy.base_session.BaseSession.request') as mock_request:
            mock_request.return_value = Response()
            mock_request.return_value._content = b'[]'

            self.assertRaises(exceptions.HTTPError, AgentSession.get_agent, AgentSession, 'client_id')

    def test_get_agent_when_receive_data_should_return_a_list_with_dict_info(self):
        with patch('pinkopy.base_session.BaseSession.request') as mock_request:
            mock_request.return_value = Response()
            mock_request.return_value._content = b'{"agentProperties": [{"key_1": "value_1"}]}'

            expected = [{'key_1': 'value_1'}]
            result = AgentSession.get_agent(AgentSession, 'client_id')
            self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()

