# ---------------------------------------------------
# Install dependencies
# pip install langgraph langchain-groq python-dotenv
# ---------------------------------------------------

import os
import json
from dotenv import load_dotenv
from typing import TypedDict, Annotated

from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage
from langchain_groq import ChatGroq

# ---------------------------------------------------
# LOAD ENV + LLM
# ---------------------------------------------------

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
)

# ---------------------------------------------------
# LONG TERM MEMORY STORAGE (FILE DATABASE)
# ---------------------------------------------------

MEMORY_FILE = "long_term_memory.json"


def load_long_memory(user_id):
    if not os.path.exists(MEMORY_FILE):
        return {}

    with open(MEMORY_FILE, "r") as f:
        data = json.load(f)

    return data.get(user_id, {})


def save_long_memory(user_id, memory):
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {}

    data[user_id] = memory

    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ---------------------------------------------------
# SHORT TERM MEMORY (GRAPH STATE)
# ---------------------------------------------------

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    user_id: str


# ---------------------------------------------------
# LANGGRAPH NODE (LLM + MEMORY)
# ---------------------------------------------------

def chatbot_node(state: AgentState):

    user_id = state["user_id"]
    user_message = state["messages"][-1].content.lower()

    # Load long-term memory
    long_memory = load_long_memory(user_id)

    # -------- STORE NAME PERMANENTLY --------
    if "my name is" in user_message:
        name = user_message.split("my name is")[-1].strip().title()

        long_memory["name"] = name
        save_long_memory(user_id, long_memory)

        reply = f"I saved your name permanently, {name}."

    # -------- RECALL NAME --------
    elif "what is my name" in user_message:
        name = long_memory.get("name")

        if name:
            reply = f"Your name is {name}."
        else:
            reply = "I don't know your name yet."

    # -------- NORMAL LLM RESPONSE --------
    else:
        response = llm.invoke(state["messages"])
        reply = response.content

    # Save reply into short-term memory
    state["messages"].append(AIMessage(content=reply))

    return state


# ---------------------------------------------------
# BUILD LANGGRAPH
# ---------------------------------------------------

workflow = StateGraph(AgentState)

workflow.add_node("chatbot", chatbot_node)

workflow.set_entry_point("chatbot")
workflow.add_edge("chatbot", END)

app = workflow.compile()


# ---------------------------------------------------
# CHAT LOOP
# ---------------------------------------------------

state = {
    "messages": [],
    "user_id": "user_1",  # simulate logged-in user
}

print("\n✅ Long-Term Memory Chatbot Started")
print("Type 'exit' to quit\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    state["messages"].append(HumanMessage(content=user_input))

    state = app.invoke(state)

    print("AI:", state["messages"][-1].content)