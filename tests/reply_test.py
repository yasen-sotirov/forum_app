from routers.replies import view_best_reply, add_reply, view_replies_by_topic_title
import unittest
from unittest.mock import patch, Mock
from services import user_service


class TestReplies(unittest.TestCase):

    @patch('services.topic_service.topic_exists', return_value=True)
    @patch('services.topic_service.find_topic_id_by_name', return_value=42)
    @patch('services.user_service.find_user_by_id', return_value='Alice')
    @patch('data.database.read_query', return_value=[(1, 'Hello', 1)])
    def test_view_replies_by_topic_title(self, mock_read_query, mock_find_topic_id_by_name, mock_topic_exists,
                                         mock_find_user_by_id):
        # Arrange
        topic_title = 'Cardio vs. Strength'

        # Act
        result = view_replies_by_topic_title(topic_title)

        # Assert
        self.assertTrue(mock_topic_exists.called)
        self.assertFalse(mock_find_topic_id_by_name.called)
        self.assertFalse(mock_read_query.called)
        self.assertTrue(mock_find_user_by_id.called)
        self.assertEqual(result, [])

    @patch('services.topic_service.topic_exists', return_value=True)
    @patch('services.topic_service.find_topic_id_by_name', return_value=42)
    @patch('services.user_service.get_username_by_token', return_value='Alice')
    @patch('services.topic_service.find_id_nickname', return_value=[(1, 'Alice')])
    @patch('services.reply_services.insert_query', return_value=1)
    @patch('data.database.read_query', return_value=[(1, 1, 0)])
    def test_add_reply(self, mock_read_query, mock_insert_query, mock_find_id_nickname, mock_get_username_by_token,
                       mock_find_topic_id_by_name, mock_topic_exists):
        # Arrange
        topic_title = 'Cardio vs. Strength'
        reply_text = ('Both are important, but diet plays a key role. Strength training builds muscle, '
                      'which burns more calories at rest.')
        x_token = '2;petar'

        # Act
        result = add_reply(topic_title, reply_text, x_token)

        # Assert
        self.assertTrue(mock_topic_exists.called)
        self.assertTrue(mock_find_topic_id_by_name.called)
        self.assertTrue(mock_get_username_by_token.called)
        self.assertTrue(mock_find_id_nickname.called)
        self.assertTrue(mock_insert_query.called)
        self.assertFalse(mock_read_query.called)
        self.assertEqual(result, 'The reply was added successfully')

    @patch('services.topic_service.topic_exists', return_value=True)
    @patch('services.topic_service.find_topic_id_by_name', return_value=42)
    @patch('services.topic_service.find_id_nickname', return_value=[(1, 'Alice')])
    @patch('services.reply_services.read_query', return_value=[(1, 'Hello', 1)])
    @patch('services.reply_services.get_reply_text_by_id', return_value=[('Hello', 1)])
    @patch('services.user_service.find_user_by_id', return_value='Alice')
    def test_view_best_reply(self, mock_find_user_by_id, mock_get_reply_text_by_id, mock_read_query,
                             mock_find_id_nickname, mock_find_topic_id_by_name, mock_topic_exists):
        # Arrange
        topic_title = 'Cardio vs. Strength'
        x_token = '2;petar'

        # Act
        result = view_best_reply(topic_title, x_token)

        # Assert
        self.assertTrue(mock_topic_exists.called)
        self.assertTrue(mock_find_topic_id_by_name.called)
        self.assertFalse(mock_find_id_nickname.called)
        self.assertTrue(mock_read_query.called)
        self.assertTrue(mock_get_reply_text_by_id.called)
        self.assertTrue(mock_find_user_by_id.called)
        self.assertEqual(result, {'The best reply according to the topic author: Hello, by: Alice'})

    @patch('services.user_service.check_email_exist')
    def test_register_user_email_already_exists(self, mock_check_email_exist):
        # Arrange
        mock_check_email_exist.return_value = True
        email = 'boris@gmail.com'
        username = 'boris'
        password = '123321'
        date_of_birth = '2000-01-01'
        gender = 'male'

        # Act
        response = user_service.create_user(email, username, password, date_of_birth, gender)

        # Assert
        mock_check_email_exist(email)
        self.assertTrue(response)

    @patch('services.user_service.check_username_exist')
    def test_register_user_username_already_exists(self, mock_check_username_exist):
        # Arrange
        mock_check_username_exist.return_value = True
        email = 'boris@gmail.com'
        username = 'boris'
        password = '123321'
        date_of_birth = '2000-01-01'
        gender = 'male'

        # Act
        response = user_service.create_user(email, username, password, date_of_birth, gender)

        # Assert
        self.assertFalse(mock_check_username_exist.called)
        self.assertTrue(response)


if __name__ == '__main__':
    unittest.main()