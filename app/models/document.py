from pydantic import BaseModel
from langchain_core.documents import Document
from typing import Optional
from app.models.base import QueryBase

class AddDocumentRequest(BaseModel):
    page_content: str
    metadata: dict

class AddDocumentFileRequest(BaseModel):
    file_url: str 
    metadata: dict

class AddDocumentFileResponse(BaseModel):
    ids: Optional[list[str]] 

class AddDocumentResponse(BaseModel):
    ids: Optional[list[str]] 

class GetDocumentRequest(BaseModel):
    queries: list[QueryBase]
    limit: int = 10
    offset: str = ""

class GetDocumentResponse(BaseModel):
    documents: list[Document]
    
class UpdateDocumentRequest(BaseModel):
    id: str
    content: str
    metadata: dict = {}

class UpdateDocumentResponse(BaseModel):
    id: str

class DeleteDocumentRequest(BaseModel):
    ids: Optional[list[str]] = []


class DeleteDocumentResponse(BaseModel):
    status: bool 