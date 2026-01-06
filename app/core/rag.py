from typing import TypedDict, List, Optional
from app.services.area import increment_area_request_count
from langgraph.graph import MessagesState
from app.core.query_cache import *
from langchain_core.messages import SystemMessage, RemoveMessage, HumanMessage

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition

from langgraph.graph import MessagesState
from typing import Optional, Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.llm import large_llm, small_llm
from app.core.tools import doc_retriever_tool 
from langchain_core.messages import convert_to_messages
from app.core.prompt  import REWRITE_PROMPT, GENERATE_PROMPT
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition


class ConversationState(TypedDict):
    messages: MessagesState = []
    summary: str
    question: str
    response: str
    context: Optional[str]
    metadata: Optional[dict]
    area_id: Optional[str]


def generate_query_or_respond(state: ConversationState):
    messages = state.get("messages", [])
    print("QUESTION:", state["question"])
    response = (
        large_llm
        .bind_tools([doc_retriever_tool]).invoke(state["question"])
    )
    print("RESPONSE:", response)
    return {**state, "messages": messages + [HumanMessage(content=state["question"]), response]}

def generate_answer(state: ConversationState):
    question = state["question"]
    data = state["messages"][-1].content
    context = state["context"]
    prompt = GENERATE_PROMPT.format(question=question, data=data, context=context)
    response = large_llm.invoke([{"role": "user", "content": prompt}])
    add_to_cache(question, response.content, {**state["metadata"], "area_id": state["area_id"]})
    increment_area_request_count(state["area_id"])
    return {**state, "messages":state["messages"] + [response], "response": response.content}

workflow = StateGraph(ConversationState)

workflow.add_node(generate_query_or_respond)
# workflow.add_node(rewrite_question)
workflow.add_node("retrieve", ToolNode([doc_retriever_tool]))
workflow.add_node(generate_answer)
workflow.add_edge(START, "generate_query_or_respond")
workflow.add_conditional_edges(
    "generate_query_or_respond",
        tools_condition,
    {
        "tools": "retrieve",
        END: END,
    },
)

workflow.add_edge("retrieve", "generate_answer")
workflow.add_edge("generate_answer", END)

memory = InMemorySaver()
graph = workflow.compile(
    checkpointer=memory
)