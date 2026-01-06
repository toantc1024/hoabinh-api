from app.db.supabase import supabase
from app.config import config
from datetime import datetime, timedelta, timezone
import math

def get_area_limit(area_id: str):
    response = (
        supabase.table("areas")
        .select("chatbot_limit_request, created_at")
        .eq("area_id", area_id)
        .execute()
    )

    if response.data and len(response.data) > 0:
        limit = response.data[0].get("chatbot_limit_request", config.DEFAULT_REQUEST_LIMIT)
        created_at = datetime.fromisoformat(response.data[0]["created_at"]).astimezone(timezone.utc)
        return limit, created_at
    else:
        return None, None

def get_current_period_start(created_at: datetime) -> datetime:
    now = datetime.now(timezone.utc)
    days_since_created = (now - created_at).days
    periods_since_created = math.floor(days_since_created / 30)
    return created_at + timedelta(days=30 * periods_since_created)

def has_remaining_quota_for_area(area_id: str) -> bool:
    limit, created_at = get_area_limit(area_id)

    if not limit or not created_at:
        raise Exception("Area not found or missing data")

    period_start = get_current_period_start(created_at)

    res = (
        supabase.table("chatbot_request_counts")
        .select("request_count")
        .eq("area_id", area_id)
        .eq("period_start", period_start.isoformat())
        .execute()
    )

    if res.data and len(res.data) > 0:
        current_count = res.data[0]["request_count"]
    else:
        current_count = 0

    return current_count > limit

def increment_area_request_count(area_id: str):
    limit, created_at = get_area_limit(area_id)

    if not created_at:
        raise Exception("Area not found or missing created_at")

    period_start = get_current_period_start(created_at)

    # Fetch current count
    res = (
        supabase.table("chatbot_request_counts")
        .select("request_count")
        .eq("area_id", area_id)
        .eq("period_start", period_start.isoformat())
        .execute()
    )

    if res.data and len(res.data) > 0:
        current_count = res.data[0]["request_count"]
        # Update with incremented value
        supabase.table("chatbot_request_counts").update({
            "request_count": current_count + 1
        }).eq("area_id", area_id).eq("period_start", period_start.isoformat()).execute()
    else:
        supabase.table("chatbot_request_counts").insert({
            "area_id": area_id,
            "period_start": period_start.isoformat(),
            "request_count": 1
        }).execute()
