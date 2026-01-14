import os
import json
from fastmcp import Client


async def _call_mcp_tool(user_message: str, history: list[dict]) -> str:
    """
    Call MCP server's generate_marketing_plan tool.
    Uses FastMCP client to communicate with the server.
    """
    mcp_url = os.getenv("MCP_BASE_URL", "http://mcp-server:8000")
    # Add /mcp/sse for SSE transport endpoint
    mcp_sse_url = f"{mcp_url}/mcp/sse"
    
    # Convert history to JSON string for tool parameter
    history_json = json.dumps(history)
    
    async with Client(mcp_sse_url) as client:
        # Call the generate_marketing_plan tool
        result = await client.call_tool(
            "generate_marketing_plan",
            arguments={
                "user_message": user_message,
                "history": history_json
            }
        )
        
        # Extract text from result
        return result.content[0].text if result.content else ""


def mcp_generate_marketing_plan(user_message: str, history: list[dict]) -> str:
    """
    Synchronous wrapper for MCP tool call.
    Call MCP server to generate marketing plan.
    """
    import asyncio
    
    try:
        return asyncio.run(_call_mcp_tool(user_message, history))
    except Exception as e:
        raise Exception(f"MCP client error: {e}")
