from fastapi import APIRouter
from fastapi.params import Body

from app.server.controllers import user_controller
from app.server.models.user_models.user import UserPublicModel, UserModel, ResponseModel

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

@router.post('/')
async def create_user(user: UserModel = Body(...)):
    user_check = await user_controller.retrieve_single_user(username=user.username)
    if not user_check:
        user_status = await user_controller.insert_single_user(user=user)
        new_user = await user_controller.retrieve_single_user(user_id=user_status.inserted_id)
        return ResponseModel(data=UserPublicModel(**new_user), message='User created successfully')
    else:
        return ResponseModel(data=UserPublicModel(**user_check), message='User already exists')


