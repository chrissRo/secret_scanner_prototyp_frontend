import os
from datetime import datetime, timedelta

import jwt as jwt
from dotenv import load_dotenv
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import ExpiredSignatureError
from passlib.context import CryptContext

from app.server.controllers import user_controller
from app.server.models.user_models.user import UserPublicModel
from config.config import JWTConfig


class Auth:
    @property
    def oauth2scheme(self):
        return self._oauth2scheme

    @oauth2scheme.setter
    def oauth2scheme(self, value):
        self._oauth2scheme = value

    def __init__(self):
        load_dotenv()
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self._oauth2scheme = OAuth2PasswordBearer(tokenUrl='token')
        self.jwt_secret_key = os.getenv('JWT_SECRET_KEY')
        self.jwt_signing_algorithm = JWTConfig.ALGORITHM
        self.jwt_expiration_time_mins = JWTConfig.ACCESS_TOKEN_EXPIRE_MINUTES

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self._pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, plain_password) -> str:
        return self._pwd_context.hash(plain_password)

    async def authenticate_user(self, username: str, password: str) -> UserPublicModel:
        user = await user_controller.retrieve_single_user_private(username=username)
        if user:
            if self.verify_password(plain_password=password, hashed_password=user['password']):
                return UserPublicModel(username=user['username'], email=user['email'], active=user['active'])
        # Todo Error Handling

    def create_access_token(self, json_web_token: dict) -> dict:
        json_web_token.update({
                "exp": datetime.utcnow() + timedelta(minutes=self.jwt_expiration_time_mins),
                'iss': JWTConfig.ISSUER
            })
        return jwt.encode(
            payload=json_web_token,
            key=self.jwt_secret_key,
            algorithm=self.jwt_signing_algorithm
        )

    async def get_current_user(self, token: jwt) -> UserPublicModel:
        payload = jwt.decode(
            jwt=token,
            key=self.jwt_secret_key,
            algorithms=[self.jwt_signing_algorithm]
        )
        username = payload.get("sub")
        if username:
            return await user_controller.retrieve_single_user(username=username)

    async def is_authenticated(self, token: jwt) -> bool:
        try:
            current_user = await self.get_current_user(token=token)
            if current_user and current_user['active']:
                return True
            return False
        except ExpiredSignatureError:
            raise HTTPException(status_code=403, detail='token expired')


auth = Auth()
