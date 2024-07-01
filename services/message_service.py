from data.database import read_query, insert_query, update_query
from my_models.model_message import Message
from fastapi import Response
from fastapi.responses import JSONResponse

def read_messages():
    data = read_query('SELECT * FROM messages')
    return data

def create_conversation(sender_id, receiver_id):
    conversation_id = check_convo_exist(sender_id, receiver_id)
    if conversation_id is None:
        insert_query('INSERT INTO conversations(the_receiver, the_sender) VALUES (?, ?)', (receiver_id, sender_id))
        conversation_id = find_convo_id(sender_id, receiver_id)
    return conversation_id

def create_message_first(message_text, sender_id, to_convo_id, receiver_username):
    insert_query('INSERT INTO messages(text_message, the_sender, conversation_id) VALUES (?,?,?)', (message_text, sender_id, to_convo_id))
    return JSONResponse(status_code=200, content=f'Conversation was created and message sent to user: [{receiver_username}]')

def send_message_in_convo(message_text, sender_id, to_convo_id, receiver_username):
    insert_query('INSERT INTO messages(text_message, the_sender, conversation_id) VALUES (?,?,?)', (message_text, sender_id, to_convo_id))
    return {"receiver_username": receiver_username, "message_text": message_text}

def check_convo_exist(sender_id, receiver_id):
    conversation_id = read_query(
        'SELECT id_of_conversations FROM conversations WHERE (the_receiver = ? AND the_sender = ?) OR (the_receiver = ? AND the_sender = ?)',
        (receiver_id, sender_id, sender_id, receiver_id)
    )
    if conversation_id:
        return conversation_id[0][0]
    else:
        return None

def find_convo_id(sender_id, receiver_id):
    conversation_id = read_query(
        'SELECT id_of_conversations FROM conversations WHERE (the_receiver = ? AND the_sender = ?) OR (the_receiver = ? AND the_sender = ?)',
        (receiver_id, sender_id, sender_id, receiver_id)
    )
    return conversation_id[0][0]