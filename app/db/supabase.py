from supabase import create_client
from supabase.lib.client_options import ClientOptions
from app.config import config

# Initialize Supabase client using config
supabase = create_client(
    config.SUPABASE_HOST,
    config.SUPABASE_SERVICE_KEY,
    options=ClientOptions(
        auto_refresh_token=False,
        persist_session=False,
    )
)
# Access auth admin api
admin_auth_client = supabase.auth.admin