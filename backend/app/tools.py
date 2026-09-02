from langchain.tools import tool
from .rag.retrieval import retrieval



@tool 
async def retrieval_tool(query:str) -> str:
    """Search the recipe database for recipes relevant to the user's request.""" 
    recipes=await retrieval(query)
    
    return "\n\n".join(
            f"""Title: {recipe.title}
            Ingredients: {recipe.ingredients}
            Instructions: {recipe.instructions}"""
            for recipe in recipes
    )
