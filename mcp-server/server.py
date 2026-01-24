import os
import json
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from agents import field_assistant_agent
from agents.marketing.market_research_agent import MarketResearchAgent
from agents.marketing.creative_strategy_agent import CreativeStrategyAgent
from agents.marketing.evaluator_agent import EvaluatorAgent
from agents.marketing.marketing_plan_orchestrator import MarketingPlanOrchestrator

load_dotenv()

# Initialize agents as singletons
market_research_agent = MarketResearchAgent()
creative_strategy_agent = CreativeStrategyAgent()
evaluator_agent = EvaluatorAgent()
marketing_plan_orchestrator = MarketingPlanOrchestrator()

# Create MCP server
mcp = FastMCP(
    name="Marketing Plan AI Gateway",
)


# ============================================================================
# MCP TOOLS - Field Assistant
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
    context_dict = json.loads(context) if context else {}
    return field_assistant_agent.suggest_field_value(field_name, context_dict)


# ============================================================================
# MCP TOOLS - Marketing Plan Generation
# ============================================================================

@mcp.tool()
def generate_marketing_plan(product_data: str, auto_iterate: bool = False) -> str:
    """
    Generate a complete 12-section marketing plan from product data.
    
    Args:
        product_data: JSON string containing product information
        auto_iterate: If True, automatically improve plan based on evaluation
    
    Returns:
        JSON string of the complete marketing plan
    """
    product_dict = json.loads(product_data)
    marketing_plan = marketing_plan_orchestrator.generate_marketing_plan(
        product_dict, 
        auto_iterate=auto_iterate
    )
    return json.dumps(marketing_plan, ensure_ascii=False)


@mcp.tool()
def conduct_market_research(product_data: str) -> str:
    """
    Conduct comprehensive market research including SWOT, competitor analysis, and personas.
    
    Args:
        product_data: JSON string containing product information
    
    Returns:
        JSON string with market research results
    """
    product_dict = json.loads(product_data)
    research = market_research_agent.conduct_full_research(product_dict)
    return json.dumps(research, ensure_ascii=False)


@mcp.tool()
def develop_marketing_strategy(product_data: str, research_data: str) -> str:
    """
    Develop marketing strategy including positioning, messaging, and marketing mix.
    
    Args:
        product_data: JSON string containing product information
        research_data: JSON string containing market research results
    
    Returns:
        JSON string with marketing strategy
    """
    product_dict = json.loads(product_data)
    research_dict = json.loads(research_data)
    strategy = creative_strategy_agent.develop_full_strategy(product_dict, research_dict)
    return json.dumps(strategy, ensure_ascii=False)


@mcp.tool()
def evaluate_marketing_plan(product_data: str, research_data: str, strategy_data: str) -> str:
    """
    Evaluate marketing plan quality, consistency, and ethics.
    
    Args:
        product_data: JSON string containing product information
        research_data: JSON string containing market research
        strategy_data: JSON string containing marketing strategy
    
    Returns:
        JSON string with evaluation results and recommendations
    """
    product_dict = json.loads(product_data)
    research_dict = json.loads(research_data)
    strategy_dict = json.loads(strategy_data)
    evaluation = evaluator_agent.evaluate_full_plan(product_dict, research_dict, strategy_dict)
    return json.dumps(evaluation, ensure_ascii=False)


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

