from typing import List
from pydantic import BaseModel

class Course(BaseModel):
    direction: str
    value: float

class ExchangeData(BaseModel):
    exchanger: str
    courses: List[Course]

