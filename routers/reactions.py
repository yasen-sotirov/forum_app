from fastapi import APIRouter, Header, Query, Path
from fastapi.responses import JSONResponse
from services import reaction_service
from services.user_service import get_id_by_token
from authentication.authenticator import get_user_or_raise_401
 
reactions_router = APIRouter(prefix='/reactions',tags={'Everything available for Reactions'})
 
@reactions_router.put('/replies/{id_of_replies}/react', description='Add a reaction to a reply')
async def add_reaction_to_reply(
    id_of_replies: int = Path(..., description="ID of the reply to react to"),
    x_token: str = Header(..., description="User's authentication token"),
    Upvote: int = Query(..., description="Upvote (1) or Downvote (-1)"),
):
    user = get_user_or_raise_401(x_token)
    result = reaction_service.create_reply_reaction(id_of_replies, x_token, Upvote, Upvote)  
    return JSONResponse(content=result)




