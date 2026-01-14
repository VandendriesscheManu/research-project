import os
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from agents import marketing_agent

load_dotenv()

# Create MCP server
mcp = FastMCP(
    name="Marketing Plan AI Gateway",
)


# ============================================================================
# MCP TOOLS - Register agent methods as MCP tools
# ============================================================================

@mcp.tool()
def generate_marketing_plan(user_message: str, history: str = "[]") -> str:
    """
    Generate a comprehensive marketing plan based on user input.
    This tool delegates to the MarketingAgent.
    """
    return marketing_agent.generate_plan(user_message, history)


# ============================================================================
# MCP RESOURCES - Expose agent data as resources
# ============================================================================

@mcp.resource("prompt://system")
def get_system_prompt() -> str:
    """Get the system prompt for the marketing consultant."""
    return marketing_agent.system_prompt


# ============================================================================
# MCP PROMPTS - Reusable prompt templates
# ============================================================================

@mcp.prompt()
def marketing_consultation(product_details: str) -> str:
    """Generate a structured marketing consultation prompt."""
    return marketing_agent.get_consultation_prompt(product_details)


if __name__ == "__main__":
    transport = "stdio"
    if transport == "stdio":
        print("Running MCP server with stdio transport")
        mcp.run(transport="stdio")
    elif transport == "streamable-http":
        print("Running MCP server with Streamable HTTP transport")
        mcp.run(transport="streamable-http")
    else:
        raise ValueError(f"Unknown transport: {transport}")

