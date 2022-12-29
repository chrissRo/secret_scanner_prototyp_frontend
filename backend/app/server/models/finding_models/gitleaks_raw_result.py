from datetime import datetime

from pydantic import Field, EmailStr, PositiveFloat, PositiveInt
from app.server.models.finding_models.raw_result import RawResultModel


class GitleaksRawResultModel(RawResultModel):
    Description: str = Field(...)
    StartLine: PositiveInt = Field(...)
    EndLine: PositiveInt = Field(...)
    StartColumn: PositiveInt = Field(...)
    EndColumn: int = Field(...)
    Match: str = Field(...)
    Secret: str = Field(...)
    File: str = Field(...)
    # SymlinkFile: str = Field(...)
    Commit: str = Field(...)
    Entropy: PositiveFloat = Field(...)
    Author: str = Field(...)
    Email: EmailStr = Field(...)
    Date: datetime = Field(...)
    Message: str = Field(...)
    Tags: list[str] = Field(...)
    RuleID: str = Field(...)
    Fingerprint: str = Field(...)
