from fastapi import APIRouter, HTTPException, Depends
from app.models.visitor_logs import *
from app.services.visitor_logs import *

router = APIRouter(prefix="/visitor-logs", tags=["visitor-logs"])

@router.post("/add", response_model=AddVisitorLogResponse)
async def handle_add_log(request: AddVisitorLogRequest):
    return add_visitor_log(request)

