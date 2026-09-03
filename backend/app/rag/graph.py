from typing import Literal
from langchain.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph
from pydantic import BaseModel, Field
from ..tools import retrieval_tool, web_search_tool


class RouteDecision(BaseModel):
    route: Literal[
        "recipe_search",
        "web_search",
        "normal_chat",
    ]

    search_query: str = Field(
        description="A standalone search query containing relevant conversation context."
    )