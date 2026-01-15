import os
import json
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def _call_suggest_field(field_name: str, context: dict) -> str:
    """
    Call MCP server's suggest_field_value tool using stdio transport.
    """
    # Convert context to JSON string
    context_json = json.dumps(context)
    
    # Define server parameters for stdio transport
    server_params = StdioServerParameters(
        command="docker",
        args=["exec", "-i", "mcp-server", "python", "server.py"],
    )
    
    # Connect to MCP server via stdio
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection
            await session.initialize()
            
            # Call the suggest_field_value tool
            result = await session.call_tool(
                "suggest_field_value",
                arguments={
                    "field_name": field_name,
                    "context": context_json
                }
            )
            
            # Extract text from result
            return result.content[0].text if result.content else ""


def mcp_suggest_field(field_name: str, context: dict) -> str:
    """
    Synchronous wrapper for field suggestion via MCP.
    """
    try:
        return asyncio.run(_call_suggest_field(field_name, context))
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        raise Exception(f"MCP client error: {str(e)}\n\nFull traceback:\n{error_details}")
