import unittest
from unittest.mock import Mock, patch
from services import topic_service
from my_models.model_topic import Topic


class TestTopicService(unittest.TestCase):

    @patch('services.topic_service.read_query')
    def test_read_topic(self, mock_read_query):
        # Arrange
        mock_read_query.return_value = [(1, 'Title 1', 'Text 1', '2023-11-01', 'Category 1', 1)]

        # Act
        topics = topic_service.read_topic()

        # Assert
        self.assertTrue(mock_read_query.called)
        self.assertEqual(len(topics), 1)

    @patch('services.topic_service.read_query')
    @patch('services.topic_service.category_exists')
    def test_create_topic_valid_category(self, mock_category_exists, mock_read_query):
        # Arrange
        mock_category_exists.return_value = True
        mock_read_query.return_value = []

        title = 'Cardio vs. Strength'
        topic_text = "I'm trying to decide between cardio and strength training. What's more effective for weight loss?"
        date_of_creation = '2023-01-12 00:00:00'
        name_of_category = 'Fitness'
        username = 'boris'

        
        mock_read_query.return_value = [(1,)]  

        # Act
        response = topic_service.create_topic(title, topic_text, date_of_creation, name_of_category, username)

        # Assert
        self.assertTrue(mock_category_exists.called)
        self.assertTrue(mock_read_query.called)
        self.assertIsInstance(response, Topic)

    @patch('services.topic_service.read_query')
    def test_topic_exists_existing_topic(self, mock_read_query):
        # Arrange
        title = 'Existing Topic'
        mock_read_query.return_value = [(1, title, 'Text', '2023-11-01', 'Category 1', 1)]

        # Act
        exists = topic_service.topic_exists(title)

        # Assert
        self.assertTrue(mock_read_query.called)
        self.assertTrue(exists)

    @patch('services.topic_service.read_query')
    def test_topic_exists_non_existing_topic(self, mock_read_query):
        # Arrange
        title = 'Non-existing Topic'
        mock_read_query.return_value = []

        # Act
        exists = topic_service.topic_exists(title)

        # Assert
        self.assertTrue(mock_read_query.called)
        self.assertFalse(exists)

    @patch('services.topic_service.read_query')
    def test_search_topics_by_title(self, mock_read_query):
        # Arrange
        mock_read_query.return_value = [(1, 'Topic 1', 'Text 1', '2023-11-01', 'Category 1', 1),
                                        (2, 'Topic 2', 'Text 2', '2023-11-02', 'Category 2', 2)]

        search_query = 'Topic 1'

        # Act
        topics = topic_service.search_by_topic(search_query)

        # Assert
        self.assertTrue(mock_read_query.called)
        self.assertEqual(len(topics), 2)

    @patch('services.topic_service.read_query')
    def test_sort_topics_descending(self, mock_read_query):
        # Arrange
        mock_read_query.return_value = []

        # Act
        topics = topic_service.sort_by_topic('Descending')

        # Assert
        self.assertTrue(mock_read_query.called)


if __name__ == '__main__':
    unittest.main()