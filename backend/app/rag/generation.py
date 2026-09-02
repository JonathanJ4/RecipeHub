from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from uuid import uuid4

from ..tools import retrieval_tool, web_search_tool

memory = InMemorySaver()

model = ChatOpenAI(
    model="qwen/qwen3-8b",
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio",
    temperature=0,
)


agent = create_agent(
    model=model,
    tools=[retrieval_tool, web_search_tool],
    system_prompt=(
        "You are a helpful recipe assistant. "
        "Use retrieval_tool when the user wants recipes, ingredients, or instructions "
        "from the internal recipe database. "
        "Use web_search_tool for current, recent, or external information. "
        "Answer greetings and normal conversation directly without using a tool. "
        "Base factual answers on the tool results and include source URLs when web search is used."
    ),
    checkpointer=memory,
)


async def generation(
    query: str,
    conversation_id: str | None = None,
) -> tuple[str, str]:
    if conversation_id is None:
        conversation_id = str(uuid4())

    result = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": query,
                }
            ]
        },
        config={
            "configurable": {
                "thread_id": conversation_id,
            }
        },
    )

    answer = result["messages"][-1].content
    return answer, conversation_id
