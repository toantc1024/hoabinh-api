from app.services.base import query_builder
from app.db.qdrant import client
from app.db.qdrant import cache_vector_store
from app.models.chat import *
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import models


def get_chat_cache(request: GetChatCacheRequest):
    records, point_id = cache_vector_store.client.scroll(
        collection_name=cache_vector_store.collection_name,
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
    return GetChatCacheResponse(questions=documents, next_offset_id=point_id if point_id else "")

def delete_chat_cache(request: DeleteChatCacheRequest):
    is_deleted = cache_vector_store.delete(
        ids=request.uuids
    )
    return DeleteChatCacheResponse(status=is_deleted)