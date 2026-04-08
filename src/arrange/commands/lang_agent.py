"""arrange lang-agent — LangGraph AI agent with tool stubs & Ollama config."""

from arrange.utils import (
    check_uv,
    create_dirs,
    ensure_venv_exists,
    print_banner,
    print_done,
    run,
    write_file,
)

# ── Templates ────────────────────────────────────────────────────────

AGENT_PY = '''\
"""LangGraph AI Agent."""

from langgraph.graph import StateGraph, END
from langchain_community.llms import Ollama
from typing import TypedDict, Annotated
import operator


class AgentState(TypedDict):
    """State passed between nodes in the graph."""
    messages: Annotated[list, operator.add]
    current_tool: str
    result: str


def reasoning_node(state: AgentState) -> dict:
    """Main reasoning node — decides what to do next."""
    llm = Ollama(model="llama3")
    messages = state["messages"]
    response = llm.invoke(str(messages))
    return {"messages": [response], "result": response}


def tool_node(state: AgentState) -> dict:
    """Execute the selected tool."""
    tool_name = state.get("current_tool", "")
    # TODO: Import and run tools from tools/
    return {"messages": [f"Executed tool: {tool_name}"], "result": ""}


def should_continue(state: AgentState) -> str:
    """Decide whether to continue or end."""
    # TODO: Implement continuation logic
    return END


# Build the graph
graph = StateGraph(AgentState)
graph.add_node("reason", reasoning_node)
graph.add_node("tool", tool_node)
graph.set_entry_point("reason")
graph.add_conditional_edges("reason", should_continue, {"tool": "tool", END: END})
graph.add_edge("tool", "reason")

agent = graph.compile()

if __name__ == "__main__":
    result = agent.invoke({"messages": ["Hello! What can you help me with?"], "current_tool": "", "result": ""})
    print(result["result"])
'''

TOOL_SEARCH = '''\
"""Example search tool for the agent."""


def search(query: str) -> str:
    """Search the web for information.

    TODO: Implement with your preferred search API.
    """
    return f"Search results for: {query}"
'''

TOOL_CALCULATOR = '''\
"""Example calculator tool for the agent."""


def calculate(expression: str) -> str:
    """Evaluate a math expression safely."""
    try:
        result = eval(expression, {"__builtins__": {}})  # noqa: S307
        return str(result)
    except Exception as e:
        return f"Error: {e}"
'''

MEMORY_INIT = '''\
"""Memory / checkpointing utilities for the agent."""

import json
from pathlib import Path

MEMORY_DIR = Path(__file__).parent


def save_checkpoint(state: dict, name: str = "latest") -> None:
    """Save agent state to a JSON file."""
    path = MEMORY_DIR / f"{name}.json"
    path.write_text(json.dumps(state, indent=2, default=str))


def load_checkpoint(name: str = "latest") -> dict | None:
    """Load agent state from a JSON file."""
    path = MEMORY_DIR / f"{name}.json"
    if path.exists():
        return json.loads(path.read_text())
    return None
'''

ENV_FILE = '''\
# Ollama configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3

# Alternative: OpenAI
# OPENAI_API_KEY=your-key-here
# OPENAI_MODEL=gpt-4
'''


def run_command() -> None:
    """Scaffold a LangGraph AI agent project."""
    print_banner("lang-agent", "LangGraph AI agent with tool stubs & Ollama")

    check_uv()
    ensure_venv_exists()

    # Install agent dependencies
    run("uv add langgraph langchain-community")

    # Create directory structure
    create_dirs("tools", "memory")

    # Create files
    write_file("agent.py", AGENT_PY)
    write_file("tools/__init__.py", "")
    write_file("tools/search.py", TOOL_SEARCH)
    write_file("tools/calculator.py", TOOL_CALCULATOR)
    write_file("memory/__init__.py", MEMORY_INIT)
    write_file(".env", ENV_FILE)

    print_done()
