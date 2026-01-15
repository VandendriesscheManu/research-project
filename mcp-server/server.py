import os
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from agents import field_assistant_agent

load_dotenv()

# Create MCP server
mcp = FastMCP(
    name="Marketing Plan AI Gateway",
)


# ============================================================================
# MCP TOOLS - Register agent methods as MCP tools
# ============================================================================

@mcp.tool()
def suggest_field_value(field_name: str, context: str = "{}") -> str:
    """
    Suggest a value for a specific form field based on already filled fields.
    
    Args:
        field_name: The field to generate a suggestion for
        context: JSON string of already filled fields
    
    Returns:
        AI-generated suggestion for the field
    """
    import json
    context_dict = json.loads(context) if context else {}
    return field_assistant_agent.suggest_field_value(field_name, context_dict)


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

