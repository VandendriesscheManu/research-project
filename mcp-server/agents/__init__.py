"""
AI Agents Module
Import and initialize all agents here
"""
from .field_assistant_agent import FieldAssistantAgent

# Initialize agent
field_assistant_agent = FieldAssistantAgent()

# Export for easy import
__all__ = ['field_assistant_agent', 'FieldAssistantAgent']
