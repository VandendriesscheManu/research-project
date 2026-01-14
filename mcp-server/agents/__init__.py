"""
AI Agents Module
Import and initialize all agents here
"""
from .marketing_agent import MarketingAgent

# Initialize agents
marketing_agent = MarketingAgent()

# Export for easy import
__all__ = ['marketing_agent', 'MarketingAgent']
