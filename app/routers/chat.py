from fastapi import APIRouter, HTTPException, Depends
from app.dependencies.auth import get_admin_user
from app.core.query_cache import find_in_cache
from app.services.area import *
import uuid
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from langchain_core.messages import AIMessageChunk
import json
from app.models.chat import *
from app.services.chat import *

from app.core.rag import graph
from app.services.area import *


router = APIRouter(prefix="/chats", tags=["chats"])

@router.post("/ask")
async def ask(request: AskRequest):
    cached_answer = find_in_cache(request.question)
    if cached_answer is not None: 
        return StreamingResponse(iter([cached_answer]), media_type="text/plain")

    is_reach_limit = has_remaining_quota_for_area(request.area_id)
    if is_reach_limit:
        return StreamingResponse(iter([config.LIMIT_REACH_MESSAGE]), media_type="text/plain")
    
    async def event_stream():
        state = {"question": request.question, "context": request.context, "metadata": request.metadata, "area_id": request.area_id}
        for chunk, step in graph.stream(state, stream_mode="messages", config={
             "configurable": {"thread_id": request.thread_id}
        }):
            if isinstance(chunk, AIMessageChunk):
                yield chunk.content

    return StreamingResponse(event_stream(), media_type="text/plain")

@router.post("/cache", response_model=GetChatCacheResponse)
def get_cache(request: GetChatCacheRequest):
    return get_chat_cache(request)

@router.delete("/cache", response_model=DeleteChatCacheResponse, dependencies=[Depends(get_admin_user)])
def get_cache(request: DeleteChatCacheRequest):
    return delete_chat_cache(request)

