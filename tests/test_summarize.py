import unittest
from unittest.mock import patch, MagicMock
import types, sys

# Provide a dummy config module so summarize imports work
config_stub = types.ModuleType('config')
config_stub.OPENAI_API_KEY = 'test-key'
config_stub.TWILIO_SID = 'sid'
config_stub.TWILIO_AUTH_TOKEN = 'token'
config_stub.TWILIO_FROM_NUMBER = '+10000000000'
config_stub.TO_PHONE_NUMBER = '+10000000001'
sys.modules['config'] = config_stub

import summarize

class TestSummarizeChat(unittest.TestCase):
    @patch('summarize.client.chat.completions.create')
    def test_returns_mocked_message(self, mock_create):
        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        mock_message.content = 'mocked summary'
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        mock_create.return_value = mock_response

        result = summarize.summarize_chat('hello')
        self.assertEqual(result, 'mocked summary')
        mock_create.assert_called_once()

if __name__ == '__main__':
    unittest.main()
