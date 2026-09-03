from uuid import uuid4

from .graph import graph


async def generation(
    query: str,
    conversation_id: str | None = None,
) -> tuple[str, str]:
    if conversation_id is None:
        conversation_id = str(uuid4())

    result = await graph.ainvoke(
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
