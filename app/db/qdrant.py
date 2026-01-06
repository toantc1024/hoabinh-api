from app.core.embedding import embeddings
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from app.config import config
from langchain_qdrant import QdrantVectorStore

# Initialize Qdrant client using config
client = QdrantClient(url=config.QDRANT_ENDPOINT, api_key=config.QDRANT_API_KEY)

# SETUP COLLECTIONS

## CHUNK COLLECTION
if not client.collection_exists(config.CHUNK_COLLECTION_NAME):
   client.create_collection(
      collection_name=config.CHUNK_COLLECTION_NAME,
      vectors_config=VectorParams(size=config.EMBEDDING_SIZE, distance=Distance.COSINE),
   )

## CACHE COLLECTION
if not client.collection_exists(config.CACHE_COLLECTION_NAME):
   client.create_collection(
      collection_name=config.CACHE_COLLECTION_NAME,
      vectors_config=VectorParams(size=config.EMBEDDING_SIZE, distance=Distance.COSINE),
   )
   
doc_vector_store = QdrantVectorStore(
    client=client,
    collection_name=config.CHUNK_COLLECTION_NAME,
    embedding=embeddings,
)

cache_vector_store = QdrantVectorStore(
    client=client,
    collection_name=config.CACHE_COLLECTION_NAME,
    embedding=embeddings,
)