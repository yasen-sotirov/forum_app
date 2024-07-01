from pydantic import BaseModel

class Reaction(BaseModel):
    id_of_likes: int
    UpVote: int
    DownVote: int
    new_user_id: int
    id_of_replies: int

    @classmethod
    def from_query_result(cls, id_of_likes, UpVote, DownVote, new_user_id, id_of_replies):
        return cls(
            id_of_likes=id_of_likes,
            UpVote=UpVote,
            DownVote=DownVote,
            new_user_id=new_user_id,
            id_of_replies=id_of_replies
        )