from pydantic import BaseModel, Field


class TokenModel(BaseModel):
    access_token: str = Field(...)
    token_type: str = Field(...)

class TokenDataModel(BaseModel):
    username: str = Field(...)
