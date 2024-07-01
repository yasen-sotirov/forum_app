import unittest
from unittest.mock import patch, Mock
from services.reaction_service import create_reply_reaction, reaction_exists, read_reactions_for_reply
from data.database import read_query, update_query
from my_models.model_reaction import Reaction


class TestReactionService(unittest.TestCase):

    @patch('services.reaction_service.read_query')
    def test_reaction_exists(self, mock_read_query):
        # Arrange
        id_of_replies = 1
        user_id = 2
        mock_read_query.return_value = [(1, 0)]

        # Act
        result = reaction_exists(id_of_replies, user_id)

        # Assert
        self.assertTrue(mock_read_query.called)
        self.assertEqual(result, [(1, 0)])

    @patch('services.reaction_service.update_query')
    @patch('services.reaction_service.reaction_exists')
    def test_create_reply_reaction_upvote(self, mock_reaction_exists, mock_update_query):
        # Arrange
        id_of_replies = 1
        x_token = "1;boris"
        upvote = -1
        # Assume 
        mock_reaction_exists.return_value = [(1, 0)]

        # Act
        result = create_reply_reaction(id_of_replies, x_token, upvote, upvote)

        # Assert
        self.assertTrue(mock_reaction_exists.called)
        self.assertTrue(mock_update_query.called)
        self.assertEqual(result, "Changed UpVote to DownVote successfully")

    @patch('services.reaction_service.update_query')
    @patch('services.reaction_service.reaction_exists')
    def test_create_reply_reaction_downvote(self, mock_reaction_exists, mock_update_query):
        # Arrange
        id_of_replies = 1
        x_token = "1;boris"
        downvote = -1
        mock_reaction_exists.return_value = [(0, 1)]

        # Act
        result = create_reply_reaction(id_of_replies, x_token, downvote, downvote)

        # Assert
        self.assertTrue(mock_reaction_exists.called)
        self.assertTrue(mock_update_query.called)
        self.assertEqual(result, "You have already downvoted this reply.")

    @patch('services.reaction_service.update_query')
    @patch('services.reaction_service.reaction_exists')
    def test_create_reply_reaction_change_upvote_to_downvote(self, mock_reaction_exists, mock_update_query):
        # Arrange
        id_of_replies = 1
        x_token = "1;boris"
        downvote = -1
        mock_reaction_exists.return_value = [(1, 0)]

        # Act
        result = create_reply_reaction(id_of_replies, x_token, downvote, downvote)

        # Assert
        self.assertTrue(mock_reaction_exists.called)
        self.assertTrue(mock_update_query.called)
        self.assertEqual(result, "Changed UpVote to DownVote successfully")

    @patch('services.reaction_service.update_query')
    @patch('services.reaction_service.reaction_exists')
    def test_create_reply_reaction_change_downvote_to_upvote(self, mock_reaction_exists, mock_update_query):
        # Arrange
        id_of_replies = 1
        x_token = "1;boris"
        upvote = 1
        mock_reaction_exists.return_value = [(0, -1)]

        # Act
        result = create_reply_reaction(id_of_replies, x_token, upvote, upvote)

        # Assert
        self.assertTrue(mock_reaction_exists.called)
        self.assertTrue(mock_update_query.called)
        self.assertEqual(result, "Changed DownVote to UpVote successfully")

    @patch('services.reaction_service.update_query')
    @patch('services.reaction_service.reaction_exists')
    def test_create_reply_reaction_already_upvoted(self, mock_reaction_exists, mock_update_query):
        # Arrange
        id_of_replies = 1
        x_token = "1;boris"
        upvote = 1
        mock_reaction_exists.return_value = [(1, 0)]

        # Act
        result = create_reply_reaction(id_of_replies, x_token, upvote, upvote)

        # Assert
        self.assertTrue(mock_reaction_exists.called)
        self.assertFalse(mock_update_query.called)
        self.assertEqual(result, "You have already upvoted this reply.")

    @patch('services.reaction_service.update_query')
    @patch('services.reaction_service.reaction_exists')
    def test_create_reply_reaction_already_downvoted(self, mock_reaction_exists, mock_update_query):
        # Arrange
        id_of_replies = 1
        x_token = "4;alice"
        upvote = -1
        mock_reaction_exists.return_value = [(0, -1)]

        # Act
        result = create_reply_reaction(id_of_replies, x_token, upvote, upvote)

        # Assert
        self.assertTrue(mock_reaction_exists.called)
        self.assertFalse(not mock_update_query.called)
        self.assertEqual(result, "You have already downvoted this reply.")

    @patch('services.reaction_service.update_query')
    @patch('services.reaction_service.reaction_exists')
    def test_create_reply_reaction_invalid_vote_value(self, mock_reaction_exists, mock_update_query):
        # Arrange
        id_of_replies = 1
        x_token = "1;boris"
        vote_value = 0
        mock_reaction_exists.return_value = []

        # Act
        result = create_reply_reaction(id_of_replies, x_token, vote_value, vote_value)

        # Assert
        self.assertTrue(mock_reaction_exists.called)
        self.assertFalse(mock_update_query.called)
        self.assertEqual(result, "Invalid vote value. Please use 1 for UpVote or -1 for DownVote.")

    @patch('services.reaction_service.read_query')
    def test_read_reactions_for_reply(self, mock_read_query):
        # Arrange
        id_of_replies = 1
        user_id = 1
        mock_read_query.return_value = [(1, 1, 1, 1, user_id)]

        # Act
        result = read_reactions_for_reply(id_of_replies, user_id)

        # Assert
        self.assertTrue(mock_read_query.called)
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], Reaction)
        self.assertEqual(result[0].id_of_likes, 1)
        self.assertEqual(result[0].UpVote, 1)
        self.assertEqual(result[0].DownVote, 1)
        self.assertEqual(result[0].new_user_id, user_id)
        self.assertIsNotNone(result[0].id_of_replies)


if __name__ == '__main__':
    unittest.main()