from langchain.tools import tool
from rag import retrieval

retrieval_tool = tool(retrieval)