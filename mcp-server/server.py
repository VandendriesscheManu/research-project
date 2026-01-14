import os
import requests
from fastmcp import FastMCP, Context

# Initialize FastMCP server
mcp = FastMCP("Marketing Plan AI Gateway")

# Environment variables
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

SYSTEM_PROMPT = """You are a professional marketing consultant AI assistant. Your role is to create comprehensive marketing plans based on product details provided by users.

When generating a marketing plan, include:
1. Executive Summary - Brief overview of the product and marketing strategy
2. Target Audience - Demographics, psychographics, and customer personas
3. Unique Selling Proposition (USP) - What makes this product stand out
4. Marketing Channels - Recommended channels (social media, email, content marketing, paid ads, etc.)
5. Content Strategy - Types of content to create and distribution plan
6. Budget Recommendations - Suggested budget allocation across channels
7. Timeline - Phased rollout plan with milestones
8. Key Metrics - KPIs to track success

Be professional, thorough, and actionable. Tailor your recommendations to the specific product details provided.
"""


def _call_llm(messages: list[dict]) -> str:
    """Call Ollama LLM with prepared messages."""
    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False,
    }
    r = requests.post(f"{OLLAMA_BASE_URL}/api/chat", json=payload, timeout=120)
    r.raise_for_status()
    data = r.json()
    return data["message"]["content"]


@mcp.tool()
def generate_marketing_plan(user_message: str, history: str = "") -> str:
    """
    Generate a comprehensive marketing plan based on user input.
    This is the main orchestration tool that calls the LLM.
    """
    # Parse history from JSON string to list
    import json
    history_list = json.loads(history) if history else []
    
    # Build messages for LLM
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    # Add history (last 12 messages)
    for m in history_list[-12:]:
        role = m.get("role", "user")
        content = m.get("content", "")
        if role in ("user", "assistant", "system") and content:
            messages.append({"role": role, "content": content})
    
    # Add current user message
    messages.append({"role": "user", "content": user_message})
    
    # Call LLM and return response
    return _call_llm(messages)


# MCP Resource - Expose the system prompt
@mcp.resource("prompt://system")
def get_system_prompt() -> str:
    """Get the system prompt for the marketing consultant."""
    return SYSTEM_PROMPT


# MCP Prompt - Reusable prompt template
@mcp.prompt()
def marketing_consultation(product_details: str) -> str:
    """Generate a structured marketing consultation prompt."""
    return f"""I need help creating a marketing plan for the following product:

{product_details}

Please provide a comprehensive marketing strategy including target audience analysis, recommended channels, budget suggestions, and success metrics."""


if __name__ == "__main__":
    # Run the server with HTTP transport for deployment
    mcp.run(transport="http", host="0.0.0.0", port=8000)

