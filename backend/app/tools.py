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
    """Search the public web for recipe follow-up information not stored in the internal database.

    Use this for detailed cooking techniques, ingredient substitutions, additional
    instructions, food-safety questions, or current external information. Do not
    use it for initial recipe discovery; use the internal recipe tool instead.
    """
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
