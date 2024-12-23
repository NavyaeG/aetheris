from pydantic import BaseModel, model_validator
from uuid import uuid4
from typing import Optional


class Alarm(BaseModel):
    
    alarmId: str = None
    alarmTime: str
    repeat: Optional[bool] = False
    day: Optional[str] = None  

    @model_validator(mode='before')
    def generateAlarmId(cls, values):
        if "alarmId" not in values:
            values["alarmId"] = uuid4().hex[:8]  
        return values