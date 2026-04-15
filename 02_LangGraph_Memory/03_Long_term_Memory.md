
### **🧠 1️⃣ Short-Term Memory (Graph State) in LangGraph**
```
🔹Long-Term Memory = information that survives beyond one execution or session.
🔹If you restart your program and the agent still remembers you → that’s long-term memory.
🔹LangGraph itself does NOT store long-term memory.
🔹It orchestrates memory access.

🔹Meaning:
    LangGraph = Brain Controller
    Database = Long-term memory

```
#### **🏗️ Where Long-Term Memory Lives**
```
🔹Unlike short-term memory (Graph State), long-term memory is stored outside LangGraph.

🔹Typical storage:
    Vector Database (semantic memory)
    SQL Database
    Redis
    Files
    Knowledge Base

🔹LangGraph reads + writes to these stores.
```

### **⭐ Two Types of Long-Term Memory**
```
1️⃣ Profile Memory (Structured Memory)
2️⃣ Semantic Memory (Vector Memory)
```

**1️⃣ Profile Memory (Structured Memory)**
```
Stores facts about user.

Example:
    {
    "name": "Rahul",
    "city": "Delhi",
    "favorite_language": "Python"
    }

Used for:
    personalization
    assistants
    copilots
```

**2️⃣ Semantic Memory (Vector Memory)**
```
Stores knowledge embeddings.

Example memories:
    past conversations
    documents
    research
    notes

Used for:
    RAG systems
    knowledge agents
```

#### ⭐**🛠️ How Long-Term Memory Works (Step-by-Step)**

*Step 1 — User provides info*
```
"My name is Rahul"
```

*Step 2 — Extract information*
```
Agent detects: name = Rahul
```

*Step 3 — Save to database*
```
memory_db["user_1"]["name"] = Rahul
```
*Step 4 — Later session*
```
User asks: "What is my name?"

Agent: Load memory → Answer using stored data
```



⚪⚫⚪  Lets learn with Code : [03_LTM.py](../code/03_LTM.py)



<!-- 🔷🔶🔹🔸⭐🔘🔴🟠🟡⚪⚫🟤🟣🔵🟢 -->