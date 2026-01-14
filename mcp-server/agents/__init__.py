"""
AI Agents Module
Import and initialize all agents here
"""
from .marketing_agent import MarketingAgent
from .field_assistant_agent import FieldAssistantAgent

# Initialize agents
marketing_agent = MarketingAgent()
field_assistant_agent = FieldAssistantAgent()

# Export for easy import
__all__ = ['marketing_agent', 'MarketingAgent']
