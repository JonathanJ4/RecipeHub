import requests 



async def generation(query,recipes):
        
        context = "\n\n".join(
        f"""
        Recipe: {recipe.name}
        Ingredients: {recipe.ingredients}
        Instructions: {recipe.instructions}
        """
        for recipe in recipes)
        
        base_url =  "http://127.0.0.1:1234/api/v1/chat"

        headers = {
                "Content-Type": "application/json"
}

        body = {
        "model": "qwen/qwen3-8b",
        "input": [
                {
                        "type":"text",
                        "content":f"""  

                                Retrieved recipes: {context}
                                User_query: {query}     
                        """
                }
        ],
        "system_prompt": "Answer the users question using the retrieved content"
}
        response = requests.post(
                base_url,
                headers=headers,
                json=body
        )
        return (response.json()['output'][1]['content'])
