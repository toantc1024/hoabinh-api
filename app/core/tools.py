from langchain.tools.retriever import create_retriever_tool
from app.db.qdrant import doc_vector_store


from langchain_core.tools import tool

@tool
def doc_retriever_tool(query:str) ->str:
    "Tìm kiếm và trả về thông tin về địa điểm lịch sử, văn hóa, du lịch, kiến thức trong cơ sở dữ liệu."
    documents = doc_vector_store.similarity_search(query, k=5)
    return "\n".join([doc.page_content for doc in documents])

