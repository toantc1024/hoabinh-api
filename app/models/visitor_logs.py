from pydantic import BaseModel

class AddVisitorLogRequest(BaseModel):
    area_id: str
    session_id: str 
    metadata: dict 

class AddVisitorLogResponse(BaseModel):
    status: bool

