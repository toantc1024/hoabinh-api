from langchain_community.embeddings import JinaEmbeddings
from app.config import config

embeddings = JinaEmbeddings(
    jina_api_key=config.JINA_AI_API_KEY, model_name="jina-embeddings-v4"
)


# import torch
# from langchain_community.embeddings import HuggingFaceBgeEmbeddings
# pick device automatically
# device = "cuda" if torch.cuda.is_available() else "cpu"

# model_name = "BAAI/bge-m3"
# model_kwargs = {"device": device}
# encode_kwargs = {"normalize_embeddings": True}

# embeddings = HuggingFaceBgeEmbeddings(
#     model_name=model_name,
#     model_kwargs=model_kwargs,
#     encode_kwargs=encode_kwargs,
# )

# print(f"Model loaded on: {device}")
