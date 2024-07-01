import unittest
from unittest.mock import patch
from services import category_service


class TestCategoryService(unittest.TestCase):


    @patch('services.category_service.read_query')
    def test_category_exists(self, mock_read_query):
        # Arrange
        category_name = 'TestCategory'
        mock_read_query.return_value = [('TestCategory',)]

        # Act
        exists = category_service.category_exists(category_name)

        # Assert
        self.assertTrue(exists)
        mock_read_query.assert_called_once_with(
            'SELECT * FROM category WHERE name_of_category = ?', (category_name,))

    @patch('services.category_service.insert_query')
    def test_create_category(self, mock_insert_query):
        # Arrange
        category_name = 'TestCategory'
        mock_insert_query.return_value = 1

        # Act
        created_category = category_service.create_category(category_name)

        # Assert
        self.assertTrue(mock_insert_query.called)
        self.assertEqual(created_category, 1)

    @patch('services.category_service.read_query')
    def test_sort_by_category(self, mock_read_query):
        # Arrange
        mock_read_query.return_value = sorted([('CategoryB',), ('CategoryA',)])

        # Act
        sorted_categories = category_service.sort_by_category('Ascending')

        # Assert
        self.assertTrue(mock_read_query.called)
        self.assertEqual(sorted_categories, [('CategoryA',), ('CategoryB',)])

    @patch('services.category_service.read_query')
    def test_get_topics_by_category_name(self, mock_read_query):
        # Arrange
        category_name = 'TestCategory'
        mock_read_query.return_value = [(1, 'TitleA', 'TextA', '2023-11-01', 'TestCategory', 1)]

        # Act
        topics = category_service.get_topics_by_category_name(category_name)

        # Assert
        self.assertTrue(mock_read_query.called)
        self.assertEqual(topics, [(1, 'TitleA', 'TextA', '2023-11-01', 'TestCategory', 1)])

    @patch('services.category_service.read_query')
    def test_search_by_categories(self, mock_read_query):
        # Arrange
        search_term = 'SearchTerm'
        mock_read_query.return_value = [('CategoryA',), ('CategoryB',)]

        # Act
        found_categories = category_service.search_by_categories(search_term)

        # Assert
        self.assertTrue(mock_read_query)
        self.assertEqual(found_categories, [('CategoryA',), ('CategoryB',)])

    @patch('services.category_service.read_query')
    def test_category_exists_return_false_when_category_not_exist(self, mock_read_query):
        # Arrange
        category_name = 'NonExistentCategory'
        mock_read_query.return_value = []

        # Act
        exists = category_service.category_exists(category_name)

        # Assert
        self.assertTrue(mock_read_query.called)
        self.assertFalse(exists)

if __name__ == '__main__':
    unittest.main()
