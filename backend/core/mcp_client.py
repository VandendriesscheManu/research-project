import os
import json
import asyncio
from datetime import datetime
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def _serialize_history(history: list[dict]) -> str:
    """
    Serialize history to JSON, handling datetime objects.
    """
    def default_serializer(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
    
    # Clean history to only include role and content
    clean_history = []
    for item in history:
        clean_history.append({
            "role": item.get("role", "user"),
            "content": item.get("content", "")
        })
    
    return json.dumps(clean_history, default=default_serializer)


async def _call_mcp_tool(user_message: str, history: list[dict]) -> str:
    """
    Call MCP server's generate_marketing_plan tool using stdio transport.
    """
    # Convert history to JSON string
    history_json = _serialize_history(history)
    
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
            
            # Call the generate_marketing_plan tool
            result = await session.call_tool(
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
    Synchronous wrapper for MCP tool call using stdio transport.
    """
    try:
        return asyncio.run(_call_mcp_tool(user_message, history))
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        raise Exception(f"MCP client error: {str(e)}\n\nFull traceback:\n{error_details}")


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
