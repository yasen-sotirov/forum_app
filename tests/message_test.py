import unittest
from unittest.mock import patch, Mock
from pydantic import json
from services import conversation_service
from services.message_service import (
    create_message_first,
    send_message_in_convo,
    check_convo_exist, create_conversation, read_messages,
)
import json


class TestMessageService(unittest.TestCase):

    @patch('services.message_service.insert_query')
    def test_create_message_first(self, mock_insert_query):
        # Arrange
        message_text = "Hello"
        sender_id = 1
        to_convo_id = 13
        receiver_username = "Alice"

        mock_insert_query.return_value = 1

        # Act
        response = create_message_first(message_text, sender_id, to_convo_id, receiver_username)

        # Assert
        self.assertTrue(mock_insert_query.called)
        self.assertEqual(response.status_code, 200)

    @patch('services.message_service.insert_query')
    def test_send_message_in_convo(self, mock_insert_query):
        # Arrange
        message_text = "Hello"
        sender_id = 1
        to_convo_id = 13
        receiver_username = "Alice"

        mock_insert_query.return_value = 1

        # Act
        response = send_message_in_convo(message_text, sender_id, to_convo_id, receiver_username)

        # Assert
        self.assertTrue(mock_insert_query.called)
        self.assertEqual(response, {"receiver_username": receiver_username, "message_text": message_text})

    @patch('services.message_service.read_query')
    def test_check_convo_exist(self, mock_read_query):
        # Arrange
        sender_id = 1
        receiver_id = 2

        mock_read_query.return_value = [(1, sender_id, receiver_id)]

        # Act
        result = check_convo_exist(sender_id, receiver_id)

        # Assert
        self.assertTrue(result)

    @patch('data.database.read_query')
    def test_messaged_users_no_messages(self, mock_read_query):
        # Arrange
        the_sender = 4

        mock_read_query.return_value = []

        # Act
        result = conversation_service.messaged_users(the_sender)

        response_data = json.loads(result.body.decode('utf-8'))

        # Assert
        expected_response = {'status_code': 404, 'content': 'There is no messages for this user'}
        self.assertEqual(result.status_code, expected_response['status_code'])
        self.assertEqual(response_data, expected_response['content'])


    @patch('services.message_service.read_query')
    def test_read_messages(self, mock_read_query):
        # Arrange
        expected_messages = [(1, "Hello", 1), (2, "Hi there!", 2)]

        mock_read_query.return_value = expected_messages

        # Act
        result = read_messages()

        # Assert
        self.assertTrue(mock_read_query.called)
        self.assertEqual(result, expected_messages)


if __name__ == '__main__':
    unittest.main()
