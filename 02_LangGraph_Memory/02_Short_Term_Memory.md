### **🧠 1️⃣ Short-Term Memory (Graph State) in LangGraph**
```
Short-term memory = the shared state object that exists while the graph is running.
It stores everything the agent currently knows during execution.

Think of it as:
    👉 the agent’s working memory
    👉 RAM of your AI workflow
```
### **🏗️ Core Idea**
```
LangGraph applications are state machines.

Instead of passing outputs manually between steps:Node A → Node B → Node C

LangGraph does: STATE → Node → Updated STATE → Next Node

The state is the memory.
```
*Example:*
```py
from typing import TypedDict

class AgentState(TypedDict):
    messages: list
    research_notes: str
    decision: str
# This structure becomes your memory container.
```



⚪⚫⚪  Lets learn with Code : [02_STM.py](../code/02_STM.py)

⚪⚫⚪  Lets learn LONG TERM MEMORY : [03_Long_term_Memory.md](./03_Long_term_Memory.md)



<!-- 🔷🔶🔹🔸🔘🔴🟠🟡⚪⚫🟤🟣🔵🟢 -->