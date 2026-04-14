
### **🧠 Persistent Memory (Checkpointing) in LangGraph**
```
Checkpointing = saving the entire graph state automatically so execution can resume later.

Think: The agent pauses → memory saved → agent resumes later exactly where it stopped.
```

### 🔶🔶🔶**What Problem Does It Solve?**
```
Normally, AI agents forget everything when:
    program crashes
    server restarts
    user closes browser
    workflow pauses
```

*Example without checkpointing:*
```
User → Step 1 → Step 2 → ❌ crash

👉 Everything lost.
```

*With Checkpointing*
```
User → Step 1 → ✅ SAVE STATE
        ↓
      crash
        ↓
Reload → Resume Step 2

👉Nothing lost.
```

### **🏗️ What Gets Saved?**
```
LangGraph saves the entire Graph State:

state = {
   "messages": [...],
   "user_name": "Rahul",
   "tool_results": {...},
   "next_step": "research"
}
```

*It stores:*
```
✅ conversation history
✅ agent decisions
✅ tool outputs
✅ workflow position
✅ intermediate reasoning
```

**🔥 Why LangGraph Checkpointing Is Special**
```
Traditional frameworks: save chat history only
LangGraph: saves execution state

Meaning it remembers: 👉 what the agent was doing
```

#### **🧠 How It Works Internally**
```
LangGraph introduces: "Checkpointer"

A storage backend that automatically saves state after each step.
```

#### **🔥Execution Flow**
```
Node runs
   ↓
State updated
   ↓
Checkpoint saved
   ↓
Next node
```

#### **🔶🔶🔶 Basic Checkpoint Example**

1️⃣ Add a Checkpointer
```py
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()
```

2️⃣ Compile Graph With Checkpointer
```py
app = workflow.compile(checkpointer=checkpointer)
Now checkpointing is enabled.
```

3️⃣ Run With Thread ID
```py
config = {
    "configurable": {
        "thread_id": "user_1"
    }
}

app.invoke(state, config=config)
```

#### **🧠 What is thread_id?**
```
Think of it as:
    conversation_id
    session_id
    user_id
    chat_id

Same thread → memory restored
New thread → new conversation
Every step becomes recoverable.
```

### **⭐Types of Checkpointers**

**In-Memory (Development)**
```py
MemorySaver()

# It is Temporary.
```

**SQLite (Local Persistence)**
```py
from langgraph.checkpoint.sqlite import SqliteSaver
SqliteSaver.from_conn_string("sqlite:///checkpoints.db")

# Saved on disk.
```

⚪⚫⚪  Lets learn  : [05_Factual_Memory](./05_Factual_memory.md)



<!-- 🔷🔶🔹🔸⭐🔘🔴🟠🟡⚪⚫🟤🟣🔵🟢 -->