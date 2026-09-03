from typing import Literal

from langchain.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph
from pydantic import BaseModel, Field

from ..tools import retrieval_tool, web_search_tool


class RouteDecision(BaseModel):
    route: Literal["recipe_search", "web_search", "normal_chat"]
    search_query: str = Field(
        description="A standalone search query that includes relevant conversation context."
    )


class RecipeState(MessagesState):
    route: str
    search_query: str
    context: str


model = ChatOpenAI(
    model="qwen/qwen3-8b",
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio",
    temperature=0,
)

router_model = model.with_structured_output(RouteDecision)


async def classify_question(state: RecipeState):
    decision = await router_model.ainvoke(
        [
            SystemMessage(
                content="""Classify the latest user message into exactly one route.

Choose recipe_search when the user wants recipe recommendations, asks what they
can make, or provides ingredients and wants matching recipes from the internal
recipe database.

Choose web_search when the user asks for extra details about a recipe, ingredient
substitutions, cooking techniques, food safety, or current information that may
not be in the internal recipe record.

Choose normal_chat for greetings, thanks, and conversation that does not require
recipe or web information.

Use the conversation history to understand follow-up questions. Also produce a
standalone search query that replaces vague words such as 'it', 'that recipe', or
'that ingredient' with the relevant details from the conversation."""
            ),
            *state["messages"],
        ]
    )

    return {
        "route": decision.route,
        "search_query": decision.search_query,
        "context": "",
    }


async def search_recipes(state: RecipeState):
    results = await retrieval_tool.ainvoke(
        {"query": state["search_query"]}
    )
    return {"context": results}


async def search_web(state: RecipeState):
    results = await web_search_tool.ainvoke(
        {"query": state["search_query"]}
    )
    return {"context": results}


async def generate_answer(state: RecipeState):
    response = await model.ainvoke(
        [
            SystemMessage(
                content=f"""You are a helpful recipe assistant.

The selected route is: {state["route"]}

Search context:
{state["context"]}

Use the search context when it is available. If no search was needed, respond
conversationally. Do not invent information that is not supported by the search
context. Include source URLs when web search was used."""
            ),
            *state["messages"],
        ]
    )
    return {"messages": [response]}


def choose_route(state: RecipeState):
    return state["route"]


memory = InMemorySaver()

builder = StateGraph(RecipeState)
builder.add_node("classify", classify_question)
builder.add_node("recipe_search", search_recipes)
builder.add_node("web_search", search_web)
builder.add_node("answer", generate_answer)

builder.add_edge(START, "classify")
builder.add_conditional_edges(
    "classify",
    choose_route,
    {
        "recipe_search": "recipe_search",
        "web_search": "web_search",
        "normal_chat": "answer",
    },
)
builder.add_edge("recipe_search", "answer")
builder.add_edge("web_search", "answer")
builder.add_edge("answer", END)

graph = builder.compile(checkpointer=memory)
