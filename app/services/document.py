from app.db.qdrant import client
from app.db.qdrant import doc_vector_store
from app.models.document import *
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import models
from app.services.base import query_builder
from langchain_community.document_loaders import PyPDFLoader
import uuid

def add_document_from_file(request: AddDocumentFileRequest):
    loader = PyPDFLoader(request.file_url)
    pages = []
    for page in loader.lazy_load():
        new_metadata = {
            **request.metadata,
            **page.metadata
        }
        page.metadata = new_metadata
        pages.append(page)

    doc_ids = doc_vector_store.add_documents(pages)
    return doc_ids

def add_document(request: AddDocumentRequest):
    doc = Document(
        page_content=request.page_content,
        metadata=request.metadata
    )
    doc_ids = doc_vector_store.add_documents([doc])
    ids = []
    for doc_id in doc_ids:
        ids.append(str(uuid.UUID(doc_id)))
    return ids

def get_document(request: GetDocumentRequest):
    records, point_id = doc_vector_store.client.scroll(
        collection_name=doc_vector_store.collection_name,
        scroll_filter=query_builder(request.queries),
        limit=request.limit,
        with_vectors=False, 
        with_payload=True,
        offset=request.offset if len(str(request.offset)) > 0 else None
    )
    documents = []
    for record in records:
        documents.append(Document(
            page_content=record.payload.get("page_content", ""),
            metadata=record.payload,
            id=record.id
        ))
    return GetDocumentResponse(documents=documents)

def delete_document(request: DeleteDocumentRequest):
    if len(request.ids) == 0:
        return True
    return doc_vector_store.delete(ids=request.ids)

def update_document(request: UpdateDocumentRequest):
    if delete_document(request=DeleteDocumentRequest(id=request.id)):
        doc = Document( 
            page_content=request.content,
            metadata=request.metadata
        )
        doc_vector_store.add_documents([doc])
    return UpdateDocumentResponse(id=request.id)

