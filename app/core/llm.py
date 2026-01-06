from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import config

large_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=config.GOOGLE_AI_API_KEY
)

small_llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=config.GOOGLE_AI_API_KEY
)   