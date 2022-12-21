from datetime import timedelta

from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.server.auth.auth import Auth, auth
from app.server.models.token_models.auth_token import TokenModel
from app.server.models.user_models.user import ErrorResponseModel

router = APIRouter()

#####################################
# POST
#####################################

@router.post('/')
async def get_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await auth.authenticate_user(username=form_data.username, password=form_data.password)
    print(user)
    if user and user.active:
        return {
            "access_token": auth.create_access_token(
                jwt_token={
                    'sub': user.username
                }),
            'token_type': 'bearer'
        }
    else:
        # Todo Error handling
        print('Invalid username or password')
        return ErrorResponseModel('NoLogin', code=403, message='Invalid Username or Password, or user inactive')

