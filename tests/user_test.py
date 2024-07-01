import unittest
from unittest.mock import Mock, patch
from my_models.model_user import User
from services import user_service


class TestUserService(unittest.TestCase):

    @patch('services.user_service.insert_query')
    def test_register_user_valid_data(self, mock_insert_query):
        # Arrange
        mock_insert_query.return_value = 1

        email = 'testuser@example.com'
        username = 'testuser'
        password = 'strongpassword'
        date_of_birth = 'None'
        gender = 'male'

        # Act
        response = user_service.create_user(email, username, password, date_of_birth, gender)

        # Assert
        self.assertTrue(mock_insert_query.called)
        self.assertIsInstance(response, User)
        self.assertEqual(response.email, email)
        self.assertEqual(response.nickname, username)
        self.assertEqual(response.password, password)
        self.assertEqual(str(response.date_of_birth), date_of_birth)
        self.assertEqual(response.gender, gender)

    @patch('services.user_service.find_by_username')
    def test_login_user_valid_credentials(self, mock_find_by_username):
        # Arrange
        mock_find_by_username.return_value = User(id=1, email='testuser@example.com', nickname='testuser',
                                                  password='strongpassword', date_of_birth='1990-01-01', gender='male')
        username = 'testuser'
        password = 'strongpassword'

        # Act
        response = user_service.try_login(username, password)

        # Assert
        self.assertTrue(mock_find_by_username.called)
        self.assertIsInstance(response, User)
        self.assertEqual(response.nickname, username)
        self.assertEqual(response.password, password)

    @patch('services.user_service.find_by_username')
    def test_login_user_invalid_credentials(self, mock_find_by_username):
        # Arrange
        mock_find_by_username.return_value = None
        username = 'testuser'
        password = 'invalidpassword'

        # Act
        response = user_service.try_login(username, password)

        # Assert
        self.assertTrue(mock_find_by_username.called)
        self.assertIsNone(response)

    @patch('services.user_service.create_user')
    @patch('services.user_service.check_email_exist')
    def test_register_user_email_already_exists(self, mock_check_email_exist, mock_create_user):
        # Arrange
        mock_check_email_exist.return_value = True
        mock_create_user.return_value = None

        email = 'boris@gmail.com'
        username = 'boris'
        password = '123321'
        date_of_birth = '2000-01-01'
        gender = 'male'

        # Act
        response = user_service.create_user(email, username, password, date_of_birth, gender)

        # Assert
        mock_check_email_exist(email)
        mock_create_user()
        self.assertIsNone(response)

    @patch('services.user_service.create_user')
    @patch('services.user_service.check_username_exist')
    def test_register_user_username_already_exists(self, mock_check_username_exist, mock_create_user):
        # Arrange
        mock_check_username_exist.return_value = True
        mock_create_user.return_value = None

        email = 'boris@gmail.com'
        username = 'boris'
        password = '123321'
        date_of_birth = '2000-01-01'
        gender = 'male'

        # Act
        response = user_service.create_user(email, username, password, date_of_birth, gender)

        # Assert
        mock_check_username_exist(username)
        mock_create_user()
        self.assertIsNone(response)


if __name__ == '__main__':
    unittest.main()
