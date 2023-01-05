from datetime import datetime
from pydantic import BaseModel, Field, validator, StrictBool

class FalsePositiveModel(BaseModel):

    isFalsePositive: StrictBool = False
    justification: str = Field(...)
    change_date: datetime = '1900-01-01 00:00:00.000000'
    
    @validator('justification')
    def false_positive_needs_justification(cls, value):
        if value == '':
            raise ValueError('Please provide justification for falsePositive')
        else:
            return value


