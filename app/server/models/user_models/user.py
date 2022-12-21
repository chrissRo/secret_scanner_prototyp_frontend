from bson import ObjectId
from pydantic import BaseModel, Field, StrictBool, EmailStr

from utils.PyObjectId import PyObjectId


class UserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str = Field(...)
    password: str = Field(...)
    active: StrictBool = False
    email: EmailStr = Field(...)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {PyObjectId: str}


class UserPublicModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str = Field(...)
    active: StrictBool = False
    email: EmailStr = Field(...)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }

def ErrorResponseModel(error: str, code, message: str):
    return {
        "error": error,
        "code": code,
        "message": message
    }