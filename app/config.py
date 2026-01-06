import os
from dotenv import load_dotenv

load_dotenv(".env", override=True)

class Configs:
    QDRANT_ENDPOINT = os.getenv("QDRANT_ENDPOINT", "")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "6333")
    SUPABASE_HOST = os.getenv("SUPABASE_HOST", "")
    SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "")
    GOOGLE_AI_API_KEY = os.getenv("GOOGLE_AI_API_KEY", "")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    JINA_AI_API_KEY = os.getenv("JINA_AI_API_KEY", "")
    JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key-here")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    DEFAULT_REQUEST_LIMIT = os.getenv("DEFAULT_REQUEST_LIMIT", 100)
    CHUNK_COLLECTION_NAME = os.getenv("CHUNK_COLLECTION_NAME", "chunks")
    CACHE_COLLECTION_NAME = os.getenv("CACHE_COLLECTION_NAME", "cache")
    LIMIT_REACH_MESSAGE = os.getenv("LIMIT_REACH_MESSAGE")
    EMBEDDING_SIZE = os.getenv("EMBEDDING_SIZE", 1024)
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:5174").split(",")
    
    
config = Configs()