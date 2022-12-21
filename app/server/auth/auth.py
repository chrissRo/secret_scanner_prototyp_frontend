import os
from datetime import datetime, timedelta

import jwt as jwt
from dotenv import load_dotenv
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from app.server.controllers import user_controller
from app.server.models.user_models.user import UserModel, UserResponseModel
from config.config import JWTConfig


class Auth:

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

    async def authenticate_user(self, username: UserModel.username, password: UserModel.password) -> UserResponseModel:
        user = await user_controller.retrieve_single_user(user_name=username)
        if user:
            if self.verify_password(plain_password=password, hashed_password=user.password):
                return UserResponseModel(username=user.username, email=user.email)
        # Todo Error Handling

    def create_access_token(self, jwt_token: dict):
        token_to_encode = jwt_token.copy()
        return jwt.encode(
            payload=token_to_encode.update({
                "exp": datetime.utcnow() + timedelta(self.jwt_expiration_time_mins)}),
            key=self.jwt_secret_key,
            algorithm=self.jwt_signing_algorithm
        )

    async def get_current_user(self) -> UserResponseModel:
        payload = jwt.decode(
            jwt=self._oauth2scheme,
            key=self.jwt_secret_key,
            algorithms=[self.jwt_signing_algorithm]
        )
        username = payload.get("sub")
        if username:
            user = await user_controller.retrieve_single_user(user_name=username)
            return UserResponseModel(username=user.username, email=user.email)


auth = Auth()
