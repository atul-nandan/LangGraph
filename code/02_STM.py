# ---------------------------------
# Install first
# pip install langgraph langchain-groq python-dotenv
# ---------------------------------

import os
from dotenv import load_dotenv
from typing import TypedDict, Annotated

from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage
from langchain_groq import ChatGroq

# ---------------------------------
# Load ENV + LLM
# ---------------------------------

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
)

# ---------------------------------
# SHORT TERM MEMORY (GRAPH STATE)
# ---------------------------------

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    user_name: str


# ---------------------------------
# NODE — MEMORY MANAGER + LLM
# ---------------------------------

def chatbot_node(state: AgentState):

    print("\n🤖 Chatbot Node Running")

    user_message = state["messages"][-1].content.lower()

    # ---- STORE NAME IN MEMORY ----
    if "my name is" in user_message:
        name = user_message.split("my name is")[-1].strip().title()
        state["user_name"] = name

        reply = f"Nice to meet you {name}! I will remember your name."

    # ---- RECALL NAME FROM MEMORY ----
    elif "what is my name" in user_message:
        if state["user_name"]:
            reply = f"Your name is {state['user_name']}."
        else:
            reply = "I don't know your name yet."

    # ---- NORMAL LLM RESPONSE ----
    else:
        response = llm.invoke(state["messages"])
        reply = response.content

    # Save AI response into memory
    state["messages"].append(AIMessage(content=reply))

    return state


# ---------------------------------
# BUILD GRAPH
# ---------------------------------

workflow = StateGraph(AgentState)

workflow.add_node("chatbot", chatbot_node)

workflow.set_entry_point("chatbot")
workflow.add_edge("chatbot", END)

app = workflow.compile()


# ---------------------------------
# INITIAL SHORT-TERM MEMORY
# ---------------------------------

state = {
    "messages": [],
    "user_name": ""
}

# ---------------------------------
# CHAT LOOP
# ---------------------------------

print("\n✅ Chat started (type 'exit' to stop)\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    state["messages"].append(HumanMessage(content=user_input))

    state = app.invoke(state)

    print("AI:", state["messages"][-1].content)