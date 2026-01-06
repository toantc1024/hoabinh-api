from app.db.qdrant  import cache_vector_store
from langchain_core.documents import Document
def add_to_cache(question, answer, metadata: dict = {}):
    cache_vector_store.add_documents([
        Document(
            page_content=question,
            metadata={**metadata, "answer": answer}
        )
    ])

def find_in_cache(question, threshold=0.98):
    results = cache_vector_store.similarity_search_with_relevance_scores(question, k=1)
    if results:
        print(results)
        doc, score = results[0]
        if score >= threshold:
            return doc.metadata.get("answer", "")
    return None

