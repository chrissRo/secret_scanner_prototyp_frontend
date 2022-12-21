from datetime import timedelta

from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.server.auth.auth import Auth, auth
from app.server.models.token_models.auth_token import TokenModel

router = APIRouter()

#####################################
# POST
#####################################

@router.post('/', response_model=TokenModel)
async def get_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(username=form_data.username, password=form_data.password)
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
