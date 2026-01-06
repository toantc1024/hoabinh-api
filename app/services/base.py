from app.db.qdrant import client
from app.db.qdrant import doc_vector_store
from app.models.document import *
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import models


def  query_builder(queries: list[QueryBase]) -> models.Filter:
    q = []
    for query in queries:
        q.append(models.FieldCondition(
            key=f"metadata.{query.key}",
            match=models.MatchValue(value=query.value)
        ))

    return models.Filter(
        must=q
    )
    