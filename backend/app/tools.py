from ddgs import DDGS
from langchain.tools import tool

from .rag.retrieval import retrieval


@tool
async def retrieval_tool(query: str) -> str:
    """Search the internal recipe database for recipes, ingredients, and instructions."""
    recipes = await retrieval(query)
    
    return "\n\n".join(
        f"""Title: {recipe.title}
Ingredients: {recipe.ingredients}
Instructions: {recipe.instructions}"""
        for recipe in recipes
    )


@tool
def web_search_tool(query: str) -> str:
    """Search the public web for current or external information not stored in the recipe database."""
    results = DDGS(timeout=10).text(
        query,
        backend="duckduckgo",
        max_results=5,
    )

    if not results:
        return "No web search results were found."

    return "\n\n".join(
        f"""Title: {result.get("title", "")}
URL: {result.get("href", "")}
Snippet: {result.get("body", "")}"""
        for result in results
    )
