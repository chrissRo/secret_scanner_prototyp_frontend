from datetime import datetime
from typing import Any, Type, Union
from pydantic import BaseModel, Field, DirectoryPath, validator, PositiveInt

from utils.PyObjectId import PyObjectId
from .gitleaks_raw_result import GitleaksRawResultModel
from .raw_result import RawResultModel
from .false_positive import FalsePositiveModel
from ...globals.global_config import AvailableScanner, InputType


class FindingModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    scannerType: AvailableScanner
    scannerVersion: str = Field(...)
    inputType: InputType
    repositoryPath: DirectoryPath = Field(...)
    repositoryName: str = Field(...)
    scanStartTime: datetime = Field(...)
    scanEndTime: datetime = Field(...)
    save_date: datetime = Field(...)
    resultRaw: Union[GitleaksRawResultModel] = Field(...)
    falsePositive: FalsePositiveModel = Field(...)

    @validator('resultRaw')
    def check_raw_type(cls, value):
        if issubclass(type(value), RawResultModel):
            return value
        else:
            raise TypeError('Wrong type for resultRaw. Must be of type RawResult')

    class Config:
        allow_population_by_field_name = True
        json_encoders = {PyObjectId: str}

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {
        "error": error,
        "code": code,
        "message": message
    }
