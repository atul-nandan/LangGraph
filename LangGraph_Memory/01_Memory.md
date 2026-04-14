### **🔶🔶🔶 What is Memory in LangGraph?**
```
In LangGraph, memory = persistent state shared between nodes during execution or across multiple runs.

Unlike classic LangChain chains where memory is attached to a chain, LangGraph treats memory as graph state.

Think of it as: A shared state object flowing through the graph.

Each node:
        reads memory
        modifies memory
        passes updated memory forward
```

### **🔶🔶🔶Core Concept: "State"**
```
LangGraph revolves around a State object.
This state acts as memory.
    ✔ conversation history
    ✔ tool outputs
    ✔ agent decisions
    ✔ intermediate reasoning
```
Example:
```py
from typing import TypedDict

class AgentState(TypedDict):
    messages: list
    user_name: str
    task_status: str
```

#### 🔘**How Memory Works Internally**
Work Flow:
```
User Input
   ↓
Node A (updates state)
   ↓
Node B (reads state)
   ↓
Node C (updates state again)
   ↓
Final Output
```
**🧠 Mental Model**
```
Think:
    LangGraph = State Machine for LLMs
    Memory = State
    Nodes = Functions that transform state
```

#### **📦 Types of Memory in LangGraph**

1️⃣ Short-Term Memory (Graph State) : [Short Term Memory](./02_Short_Term_Memory.md)

2️⃣ Persistent Memory (Checkpointing)

3️⃣ Thread-Based Memory

4️⃣ Long-Term Memory (External Storage) 

<!-- ⚪⚫⚪  Lets learn: [Nodes, Edges & State](./02_Nodes_edges_state.md) -->
<!-- 🔷🔶🔹🔸🔘🔴🟠🟡⚪⚫🟤🟣🔵🟢 -->