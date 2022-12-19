from datetime import datetime

from pydantic import BaseModel, Field, validator, StrictBool


class FalsePositiveModel(BaseModel):

    isFalsePositive: StrictBool = False
    justification: str = Field(None)
    change_date: datetime = Field(None)

    @validator('justification')
    def false_positive_needs_justification(cls, value, values):
        if values.get('isFalsePositive') is True and value == ' ':
            raise ValueError('Please provide justification for falsePositive')

    @validator('change_date')
    def check_change_date(cls, value, values):
        if values.get('isFalsePositive') is True and value == ' ':
            raise ValueError('change_date required for FalsePositive')
