from fastapi import APIRouter, Query, Header
from fastapi.responses import JSONResponse
from services import user_service,message_service
from authentication.authenticator import get_user_or_raise_401
from services.user_service import find_username_by_id

messages_router = APIRouter(prefix='/messages', tags=['Everything available for Messages'])

@messages_router.post('/')
def send_message_to_user(
    message_text: str = Query(),
    receiver_username: str = Query(),
    x_token: str = Header(),
):
    user = get_user_or_raise_401(x_token)
    receiver_id = find_username_by_id(receiver_username)
    sender_id = int(user_service.find_user_by_token(x_token))

    if sender_id == receiver_id:
        return JSONResponse(status_code=400, content='You can\'t message yourself!')

    if not receiver_id:
        return JSONResponse(status_code=400, content='No user found!')

    convo_id = message_service.check_convo_exist(sender_id, receiver_id)

    if convo_id is None:
        convo_id = message_service.create_conversation(sender_id, receiver_id)
        return message_service.create_message_first(message_text, sender_id, convo_id, receiver_username)
    else:
        return message_service.send_message_in_convo(message_text, sender_id, convo_id, receiver_username)


