import unittest
from unittest.mock import Mock, patch
from services import conversation_service
from services import message_service
import json


class TestMessagedUsers(unittest.TestCase):

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

    @patch('data.database.read_query')
    @patch('data.database.insert_query')
    def test_create_conversation_new_conversation(self, mock_insert_query, mock_read_query):
        the_sender = 3
        the_receiver = 4

        mock_read_query.return_value = []

        mock_insert_query.return_value = 7

        # Act
        id_of_conversation = message_service.create_conversation(the_sender, the_receiver)

        # Assert
        self.assertTrue(1 <= id_of_conversation <= 100)

    @patch('data.database.read_query')
    def test_conversation_exist(self, mock_read_query):
        # Arrange
        sender_id = 1
        receiver_id = 2

        mock_read_query = Mock()
        mock_read_query.return_value = [(1, sender_id, receiver_id)]

        # Act
        result = message_service.check_convo_exist(sender_id, receiver_id)

        # Assert
        self.assertTrue(result)

    @patch('data.database.read_query')
    def test_conversation_not_exist(self, mock_read_query):
        # Arrange
        sender_id = 14
        receiver_id = 15

        mock_read_query.return_value = []

        # Act
        result = message_service.check_convo_exist(sender_id, receiver_id)

        # Assert
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()