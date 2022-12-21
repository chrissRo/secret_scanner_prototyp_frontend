from app.server.auth.auth import auth
from app.server.database import user_collection
from app.server.models.user_models.user import UserModel, UserResponseModel


#####################################
# GET
#####################################

async def retrieve_single_user(user_id='', user_name='') -> UserModel:
    if user_id:
        return await user_collection.find_one({'_id': user_id})
    if user_name:
        return await user_collection.find_one({'username': user_name})


#####################################
# POST
#####################################

async def insert_single_user(user: UserModel) -> UserResponseModel:
    user.password = auth.get_password_hash(plain_password=user.password)
    user = await user_collection.insert_one(user)
    new_user = await user_collection.find_one({'_id': user.inserted_id})
    if new_user:
        return UserResponseModel(username=new_user.username, email=new_user.email)
