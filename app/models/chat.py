from supabase_auth import BaseModel
from typing import Optional
from app.models.base import QueryBase
from langchain_core.documents import Document
import uuid

class AskRequest(BaseModel):
    question: str = ""
    context: Optional[str] = ""
    metadata: Optional[dict] = {}
    thread_id: str = str(uuid.uuid4())
    area_id: Optional[str] = ""
    
class GetChatCacheRequest(BaseModel):
    queries: list[QueryBase]
    limit: int = 10
    offset: str = ""
    
class GetChatCacheResponse(BaseModel):
    questions: list[Document]
    next_offset_id: str 

class DeleteChatCacheRequest(BaseModel):
    uuids: list[str]
    
class DeleteChatCacheResponse(BaseModel):
    status: bool