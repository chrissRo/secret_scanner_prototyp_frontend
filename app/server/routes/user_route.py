from fastapi import APIRouter
from fastapi.params import Body

from app.server.controllers import user_controller
from app.server.models.user_models.user import UserPublicModel, UserModel

router = APIRouter()

#####################################
# GET
#####################################

@router.get('/{user_id}')
async def get_user(user_id: str):
    return await user_controller.retrieve_single_user(user_id=user_id)


@router.get('/')
async def get_all_user():
    return await user_controller.retrieve_all_user()


#####################################
# POST
#####################################

@router.post('/', response_model=UserPublicModel)
async def create_user(user: UserModel = Body(...)):
    user_status = await user_controller.insert_single_user(user=user)
    return await user_controller.retrieve_single_user(user_id=user_status.inserted_id)

