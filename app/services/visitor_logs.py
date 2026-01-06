from app.models.visitor_logs import AddVisitorLogRequest, AddVisitorLogResponse
from app.db.supabase import supabase
def add_visitor_log(request: AddVisitorLogRequest) -> AddVisitorLogResponse:
    entry = supabase.table("visitor_logs").select("*").eq("session_id", request.session_id).execute()
    if (entry.data):
        return AddVisitorLogResponse(status=False)

    response = (
            supabase.table("visitor_logs")
            .insert({
                "area_id": request.area_id,
                "metadata": request.metadata,
                "session_id": request.session_id
            })
            .execute()
        )
    if (response.data):
        return AddVisitorLogResponse(status=response)
    return AddVisitorLogResponse(status=False)