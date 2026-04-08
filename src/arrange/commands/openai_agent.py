"""arrange openai-agent — Modern OpenAI AI agent with tool calling."""

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
"""OpenAI Assistant Agent."""

import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define tools
def get_weather(location: str):
    """Get the current weather in a given location."""
    return f"The weather in {location} is sunny, 25°C."

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "The city and state, e.g. San Francisco, CA"},
                },
                "required": ["location"],
            },
        },
    }
]

def run_agent(prompt: str):
    messages = [{"role": "user", "content": prompt}]
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )
    
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    
    if tool_calls:
        messages.append(response_message)
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            if function_name == "get_weather":
                function_response = get_weather(location=function_args.get("location"))
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                })
        
        final_response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
        )
        return final_response.choices[0].message.content
    
    return response_message.content

if __name__ == "__main__":
    print(run_agent("What is the weather in Tokyo?"))
'''

ENV_FILE = '''\
# OpenAI configuration
OPENAI_API_KEY=your-key-here
OPENAI_MODEL=gpt-4o
'''

def run_command() -> None:
    """Scaffold an OpenAI AI agent project."""
    print_banner("openai-agent", "Modern OpenAI Agent with Function Calling")

    check_uv()
    ensure_venv_exists()

    # Install dependencies
    run("uv add openai python-dotenv")

    # Create directory structure
    create_dirs("tools")

    # Create files
    write_file("agent.py", AGENT_PY)
    write_file(".env", ENV_FILE)

    print_done()
