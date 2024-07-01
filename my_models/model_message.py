from pydantic import BaseModel

class Message(BaseModel):
    receiver_username: str
    message_text: str