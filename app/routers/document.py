from fastapi import APIRouter, HTTPException, Depends
from langchain_core.documents import Document
from app.models.document import *
from app.services.document import *
from app.db.qdrant import doc_vector_store
from app.dependencies.auth import get_admin_user
import uuid

router = APIRouter(prefix="/documents", tags=["documents"])
from app.models.document import *
# Create (Add Document)
@router.post("/", response_model=AddDocumentResponse, dependencies=[Depends(get_admin_user)])
async def create_document(request: AddDocumentRequest):
    doc_ids = add_document(request)
    return AddDocumentResponse(ids=doc_ids)

@router.post("/file", response_model=AddDocumentFileResponse, dependencies=[Depends(get_admin_user)])
async def create_document_from_file(request: AddDocumentFileRequest):
    doc_ids = add_document_from_file(request)
    return AddDocumentFileResponse(ids=doc_ids)


# Read (Get Documents)
@router.post("/query", response_model=GetDocumentResponse, dependencies=[Depends(get_admin_user)])
async def get_documents(request: GetDocumentRequest):
    return get_document(request)

# Update (Update Document)
@router.put("/update", response_model=UpdateDocumentResponse, dependencies=[Depends(get_admin_user)])
async def update_document_route(request: UpdateDocumentRequest):
    return update_document(request)

# Delete (Delete Document)
@router.delete("/delete", response_model=DeleteDocumentResponse, dependencies=[Depends(get_admin_user)])
async def delete_document_route(request:DeleteDocumentRequest):
    result = delete_document(request)
    if not result:
        raise HTTPException(status_code=404, detail="Document not found.")
    return DeleteDocumentResponse(status=result)

