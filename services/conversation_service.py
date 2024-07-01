from my_models.model_category import Category
from data.database import read_query, insert_query
from services import user_service
from fastapi.responses import JSONResponse

def messaged_users(sender_id):

    something = read_query('SELECT the_receiver FROM conversations WHERE the_sender = ?', (sender_id,))

    find_receivers = [{'Messaged Users': user_service.find_user_by_id(row[0])} for row in something]
    
    if not find_receivers:
        return JSONResponse(status_code=404,content='There is no messages for this user')
    else:
        return find_receivers
    
def conversation_by_id(conversation: int):

    get_conversation = read_query('SELECT text_message,the_sender FROM messages WHERE conversation_id = ?',(conversation,))
    conversation = [{f'{user_service.find_nickname_by_new_id(row[1])}': {row[0]}} for row in get_conversation]
    return conversation

def between_two_users(the_sender: int, the_receiver: int):

    something = read_query('SELECT id_of_conversations FROM conversations WHERE (the_sender = ? AND the_receiver = ?) OR (the_sender = ? AND the_receiver = ?)',
                           (the_sender,the_receiver, the_receiver,the_sender,)
                           )
    if not something:
        return JSONResponse(status_code=404,content='There is no conversations between these users')

    return conversation_by_id(something[0][0])
