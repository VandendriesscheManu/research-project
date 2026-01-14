"""
Marketing Agent - Handles all marketing plan generation logic
"""
import json
from .llm_client import llm_client


class MarketingAgent:
    """AI Agent specialized in creating marketing plans"""
    
    def __init__(self):
        self.llm = llm_client
        
        self.system_prompt = """You are a professional marketing consultant AI assistant. Your role is to create comprehensive marketing plans based on product details provided by users.

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
    
    def generate_plan(self, user_message: str, history: str = "[]") -> str:
        """
        Generate a comprehensive marketing plan based on user input.
        
        Args:
            user_message: The user's request for a marketing plan
            history: JSON string of conversation history
            
        Returns:
            Generated marketing plan as a string
        """
        # Parse history from JSON string to list
        history_list = json.loads(history) if history else []
        
        # Build messages for LLM
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Add history (last 12 messages)
        for m in history_list[-12:]:
            role = m.get("role", "user")
            content = m.get("content", "")
            if role in ("user", "assistant", "system") and content:
                messages.append({"role": role, "content": content})
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        # Call LLM via unified client
        return self.llm.chat(messages)
    
    def get_consultation_prompt(self, product_details: str) -> str:
        """Generate a structured marketing consultation prompt."""
        return f"""I need help creating a marketing plan for the following product:

{product_details}

Please provide a comprehensive marketing strategy including target audience analysis, recommended channels, budget suggestions, and success metrics."""
