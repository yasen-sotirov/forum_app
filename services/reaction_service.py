from data.database import read_query, update_query
from my_models.model_reaction import Reaction
from services.user_service import get_id_by_token


def reaction_exists(id_of_replies, user_id):
    data = read_query('''SELECT UpVote, DownVote
                        FROM reactions_of_replies
                        WHERE id_of_replies = ? AND new_user_id = ?''',
                      (id_of_replies, user_id))
    return data

def read_reactions_for_reply(id_of_replies, user_id):
    data = read_query('''SELECT id_of_likes, UpVote, DownVote, new_user_id
                        FROM reactions_of_replies
                        WHERE id_of_replies = ? AND new_user_id = ?''',
                      (id_of_replies, user_id))
    return [Reaction.from_query_result(*row) for row in data]


def create_reply_reaction(id_of_replies, x_token, upvote, downvote):
    user_id = get_id_by_token(x_token)
    existing_reaction = reaction_exists(id_of_replies, user_id)

    if existing_reaction:
        (current_upvote, current_downvote) = existing_reaction[0]

        if upvote == 1:
            if current_upvote == 1:
                return "You have already upvoted this reply."
            
            if current_downvote == -1:
                update_query('''UPDATE reactions_of_replies 
                                SET UpVote = 1, DownVote = 0
                                WHERE id_of_replies = ? AND new_user_id = ?''', 
                                (id_of_replies, user_id))
                return 'Changed DownVote to UpVote successfully'
            
            if current_downvote == 0:
                update_query('''UPDATE reactions_of_replies 
                                SET UpVote = 1
                                WHERE id_of_replies = ? AND new_user_id = ?''', 
                                (id_of_replies, user_id))
                return 'Upvoted successfully'

        elif upvote == -1:
            if current_upvote == 1:
                update_query('''UPDATE reactions_of_replies 
                                SET UpVote = 0, DownVote = -1
                                WHERE id_of_replies = ? AND new_user_id = ?''', 
                                (id_of_replies, user_id))
                return 'Changed UpVote to DownVote successfully'

            if current_upvote == 0:
                update_query('''UPDATE reactions_of_replies 
                                SET DownVote = -1
                                WHERE id_of_replies = ? AND new_user_id = ?''', 
                                (id_of_replies, user_id))
                return "You have already downvoted this reply."

        else:
            return "Invalid vote value. Please use 1 for UpVote or -1 for DownVote."

    else:
        if upvote == 1:
            update_query('''INSERT INTO reactions_of_replies (UpVote, DownVote, new_user_id, id_of_replies)
                            VALUES (?, ?, ?, ?)''', (1, 0, user_id, id_of_replies))
            return 'Upvoted successfully'
        elif upvote == -1:
            update_query('''INSERT INTO reactions_of_replies (UpVote, DownVote, new_user_id, id_of_replies)
                            VALUES (?, ?, ?, ?)''', (0, -1, user_id, id_of_replies))
            return 'Downvoted successfully'
        else:
            return "Invalid vote value. Please use 1 for UpVote or -1 for DownVote."


