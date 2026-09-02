import requests


async def generation(query, recipes, conversation_id=None):
    context = "\n\n".join(
        f"""Recipe: {recipe.title}
Ingredients: {recipe.ingredients}
Instructions: {recipe.instructions}"""
        for recipe in recipes
    )

    body = {
        "model": "qwen/qwen3-8b",
        "input": f"""Retrieved recipes:

        {context}

        User question: {query}""",
        "system_prompt": "Answer the user's question using the retrieved recipes.",
        "store": True,
    }

    if conversation_id:
        body["previous_response_id"] = conversation_id

    response = requests.post(
        "http://127.0.0.1:1234/v1/chat/completions",
        headers={"Content-Type": "application/json"},
        json=body,
    )
    response.raise_for_status()
    data = response.json()

    answer = next(
        item["content"]
        for item in reversed(data["output"])
        if item["type"] == "message"
    )

    return answer, data["response_id"]
