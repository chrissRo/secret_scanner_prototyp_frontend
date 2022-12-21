from fastapi import APIRouter
from fastapi.params import Body

from app.server.controllers import user_controller
from app.server.models.user_models.user import UserResponseModel, UserModel

router = APIRouter()


#####################################
# GET
#####################################

@router.get('/{user_id}', response_model=UserResponseModel)
async def get_user(user_id: str):
    return user_controller.retrieve_single_user(user_id=user_id)


#####################################
# POST
#####################################

@router.post('/', response_model=UserResponseModel)
async def create_user(user: UserModel = Body(...)):
    return user_controller.insert_single_user(user=user)
