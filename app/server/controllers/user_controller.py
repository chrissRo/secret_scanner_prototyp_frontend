from fastapi.encoders import jsonable_encoder
from app.server.auth.auth import auth
from app.server.database import user_collection
from app.server.models.user_models.user import UserModel, UserPublicModel


#####################################
# GET
#####################################

async def retrieve_single_user(user_id: str = '', username: str = '') -> UserPublicModel:
    if user_id:
        return await user_collection.find_one({'_id': user_id})
    if username:
        return await user_collection.find_one({'username': username})


async def retrieve_single_user_private(username: str) -> UserModel:
    return await user_collection.find_one({'username': username})


async def retrieve_all_user() -> list:
    users = []
    async for user in user_collection.find():
        users.append(user)
    return users


#####################################
# POST
#####################################

async def insert_single_user(user: UserModel):
    user.password = auth.get_password_hash(plain_password=user.password)
    return await user_collection.insert_one(jsonable_encoder(user))
