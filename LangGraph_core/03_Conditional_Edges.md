### **🔶🔶🔶Conditional Edges** 
```
Conditional edges are the brain of your graph — they decide dynamically which path to take based on the current state. This is what separates LangGraph from a simple linear chain.
```

#### 🔶**How Conditional Edges Work**
```
The anatomy of a conditional edge has 3 parts:

add_conditional_edges(source_node, router_function, path_map)

🔹Source_node :         "from here" 
🔹router_function :     "ask this function what to do next"
🔹path_map:             "Go here based on the answer"
```

```py
builder.add_conditional_edges(
    "agent",           # source: which node triggers this routing
    router_fn,         # router: function that inspects state → returns a string
    {                  # path map: string → next node
        "tools": "tool_executor",
        "end":   END,
        "retry": "agent"
    }
)
```

#### 🔷 **What is Router Function ?**
```
The router function is just a Python function — it can contain any logic you want.
```

### 🔶🔶🔶**Router Function Patterns**

🔷🔷🔷 **Pattern 1 — Simple String Return**

```py
def route_by_intent(state: AgentState) -> str:
    last_message = state["messages"][-1].content.lower()
    
    if "calculate" in last_message:
        return "math_node"
    elif "search" in last_message:
        return "search_node"
    else:
        return "general_node"

builder.add_conditional_edges("classifier", route_by_intent, {
    "math_node":    "math_node",
    "search_node":  "search_node",
    "general_node": "general_node"
})
```
*Explanation:*
```py
def route_by_intent(state: AgentState) -> str:

# This function checks the latest user message from the agent’s state:
```

```py
last_message = state["messages"][-1].content.lower()

# Then it decides where the agent should go next:
#     if message contains "calculate" → return "math_node"
#     if message contains "search" → return "search_node"
#     otherwise → "general_node"

# It returns a node name, not execution.
```
```py
builder.add_conditional_edges(
    "classifier",
    route_by_intent,
    {...}
)

# After the classifier node runs:
#     LangGraph calls route_by_intent(state)
#     Reads the returned string
#     Sends execution to that node
```

*Flow*
```
User message
     ↓
classifier node
     ↓
route_by_intent()
     ↓
Selected node (math/search/general)
```
------------------------------------------------------------------------------------------------



🔷🔷🔷 **Pattern 2 — List Return (Fan-out to Multiple Nodes)**
```
Return a list of strings to trigger multiple nodes in parallel:
```
```py
from typing import Literal

def fan_out_router(state: AgentState) -> list[str]:
    tasks = []
    if state["needs_summary"]:
        tasks.append("summarizer")
    if state["needs_fact_check"]:
        tasks.append("fact_checker")
    if state["needs_translation"]:
        tasks.append("translator")
    return tasks   # all run in parallel!

builder.add_conditional_edges("planner", fan_out_router, [
    "summarizer", "fact_checker", "translator"   # declare all possible targets
])
```

*Explanation:*
```py
def fan_out_router(state: AgentState) -> list[str]:

# Unlike normal routing (which returns one node),
# this router returns multiple nodes.

# 👉 Meaning: run several tasks at the same time.
```

```py
# Checking the State
tasks = []

# Create an empty list of next nodes.
```
```py
if state["needs_summary"]:
    tasks.append("summarizer")

# If summary is needed → add summarizer.

if state["needs_fact_check"]:
    tasks.append("fact_checker")

# If fact checking is needed → add fact_checker.

if state["needs_translation"]:
    tasks.append("translator")

# If translation is needed → add translator.
```
```py
# Return Value
return tasks

# Example return: ["summarizer", "translator"]
# 👉 Both nodes execute in parallel.
```

```py
# conditional edges
builder.add_conditional_edges(
    "planner",
    fan_out_router,
    ["summarizer", "fact_checker", "translator"]
)

# Meaning: 
# After the planner node runs:
    # LangGraph calls fan_out_router(state)
    # Gets a list of nodes
    # Executes all returned nodes simultaneously
```
*Execution Flow*
```
planner
   ↓
fan_out_router()
   ↓
┌──────────────┬──────────────┬──────────────┐
    summarizer   fact_checker   translator              (run in parallel)

```



------------------------------------------------------------------------------------------------



🔷🔷🔷 **Pattern 3 — Typed Literal (safer, IDE-friendly)**
```py
from typing import Literal

def route_agent(state: AgentState) -> Literal["tools", "end", "human_review"]:
    last = state["messages"][-1]
    
    if hasattr(last, "tool_calls") and last.tool_calls:
        return "tools"
    
    confidence = state.get("confidence_score", 1.0)
    if confidence < 0.5:
        return "human_review"
    
    return "end"

# No path_map needed when key == value
builder.add_conditional_edges("agent", route_agent)
```
*Explanation-*
```
When the router's return values exactly match node names, you can omit the path map entirely.
```
```
The function checks the latest agent message from the state.
If the agent requested a tool call, it routes to "tools".
It then checks the agent’s confidence score.
If confidence is low (< 0.5), it sends the task to "human_review".
Otherwise, the workflow ends, and add_conditional_edges uses the returned value to choose the next node automatically.
```

------------------------------------------------------------------------------------------------



🔷🔷🔷**Pattern 4 —  Loop Patterns**
```py
class AgentState(TypedDict):
    messages:   Annotated[list, operator.add]
    attempts:   int
    is_valid:   bool

def check_output(state: AgentState) -> str:
    if state["is_valid"]:
        return "done"
    if state["attempts"] >= 3:
        return "give_up"
    return "retry"

builder.add_node("generator", generate)
builder.add_node("validator", validate)
builder.add_node("output",    final_output)
builder.add_node("fallback",  fallback_handler)

builder.add_edge(START,        "generator")
builder.add_edge("generator",  "validator")

builder.add_conditional_edges("validator", check_output, {
    "retry":    "generator",   # ← loop back
    "done":     "output",
    "give_up":  "fallback"
})
```
*Explanation-*
```py
# 1. AgentState (Agent Memory)
class AgentState(TypedDict):

# This defines what information the agent remembers:
#     messages → conversation history
#     attempts → how many times the agent tried
#     is_valid → whether the result is correct
```
```py
# 2. Decision Function
def check_output(state: AgentState) -> str:

# This function decides what to do after validation:
#     If output is valid → "done"
#     If tried 3 times → "give_up"
#     Otherwise → "retry"
```
```py
# 3. Nodes (Steps of Agent)

# The workflow has steps:
#     generator → creates answer
#     validator → checks answer
#     output → send final result
#     fallback → backup handling if failed
```

```py
# 4. Basic Flow

# START → generator → validator

# Agent generates something, then validates it.
```

```py
# 5. Conditional Routing (Loop Logic)

# After validation:
#     "retry" → go back to generator (try again) ✅ loop
#     "done" → go to output
#     "give_up" → go to fallback
```
```
START → generator → validator ──done──→ output → END
              ↑         │
              └─retry───┘ (max 3 times)
                  |
                  └──give_up──→ fallback → END
```



------------------------------------------------------------------------------------------------



🔷🔷🔷**Self-Correcting Agent Loop**

```py
def should_continue(state: AgentState) -> str:
    messages = state["messages"]
    last = messages[-1]

    # If LLM made tool calls, execute them
    if hasattr(last, "tool_calls") and last.tool_calls:
        return "call_tools"

    # If answer is too short, ask LLM to elaborate
    if len(last.content) < 100:
        return "elaborate"

    # Otherwise we're done
    return END

builder.add_conditional_edges("llm", should_continue, {
    "call_tools": "tools",
    "elaborate":  "llm",     # loop to itself!
    END:          END
})
builder.add_edge("tools", "llm")   # tools always go back to LLM

```
⚪⚫⚪  Lets learn: [Smart Routing](./04_Smart_routing.md)


<!-- 🔷🔶🔹🔸🔘🔴🟠🟡⚪⚫🟤🟣🔵🟢 -->