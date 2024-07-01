from fastapi import APIRouter, Query, Header
from fastapi.responses import JSONResponse
from services import user_service,message_service,conversation_service
from authentication.authenticator import get_user_or_raise_401
from services.user_service import find_username_by_id

conversations_router = APIRouter(prefix='/conversations', tags=['Everything available for Conversations'])

@conversations_router.get('/nicknames',description='From here you can get all users which you messaged or messaged you.')
def view_all_messaged_users(x_token: str = Header()):
    user = get_user_or_raise_401(x_token)

    get_user = user_service.find_user_by_token(x_token)
    if_sender_exists = user_service.find_user_by_id(get_user)

    if not if_sender_exists:
        return JSONResponse(status_code=404,content='This person doesnt exist')
    else:
        return conversation_service.messaged_users(get_user)
    
@conversations_router.get('/',description='From here you can get all of your exchanged messages between different users.')
def view_conversation_between_two_users(x_token: str = Header(),the_receiver_username: str = Query()):
    user = get_user_or_raise_401(x_token)

    the_sender = user_service.find_user_by_token(x_token)
    the_receiver = user_service.find_username_by_id(the_receiver_username)
    
    if not the_receiver:
        return JSONResponse(status_code=404,content='Not a valid receiver')
    messages =  conversation_service.between_two_users(the_sender,the_receiver)

    return messages
