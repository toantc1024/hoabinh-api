
from pydantic import BaseModel

class QueryBase(BaseModel):
    key: str
    value: str
