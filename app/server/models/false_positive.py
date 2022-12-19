from datetime import datetime
from pydantic import BaseModel, Field, validator, StrictBool

class FalsePositiveModel(BaseModel):

    isFalsePositive: StrictBool = False
    justification: str = Field(...)
    change_date: datetime = Field(...)
    
    @validator('justification')
    def false_positive_needs_justification(cls, value, values):
        if values.get('isFalsePositive') is True and value == '':
            raise ValueError('Please provide justification for falsePositive')
        else:
            return value


