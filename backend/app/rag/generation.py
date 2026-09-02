from langchain.agents import create_agent
from langchain_openai import ChatOpenAI


from ..tools import retrieval_tool


model = ChatOpenAI(
    model="qwen/qwen3-8b",
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio",
    temperature=0,
)


agent = create_agent(
    model=model,
    tools=[retrieval_tool],
    system_prompt=(
        "You are a recipe assistant. "
        "Always search for relevant recipes before answering recipe questions."
    ),

)

async def generation(query: str) -> str:
    result = await agent.ainvoke({
        "messages": [
            {
                "role": "user",
                "content": query,
            }
        ]
    })

    return result["messages"][-1].content