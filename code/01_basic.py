from typing import TypedDict
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
import os

load_dotenv()

llm=ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=os.getenv("GROQ_API_KEY")
    )

class State(TypedDict):
    message: str

def chatbot(state: State):
    reply = llm.invoke(state["message"])
    return {"message": reply.content}

builder = StateGraph(State)
builder.add_node("chatbot", chatbot)
builder.set_entry_point("chatbot")
builder.add_edge("chatbot", END)

graph = builder.compile()

print(graph.invoke({"message": "What is LangGraph?"}))