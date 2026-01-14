"""
Field Assistant Agent - Helps users fill in form fields with AI suggestions
"""
from .llm_client import llm_client


class FieldAssistantAgent:
    """AI Agent that suggests field values based on context"""
    
    def __init__(self):
        self.llm = llm_client
    
    def suggest_field_value(self, field_name: str, context: dict) -> str:
        """
        Generate a suggestion for a specific field based on already filled fields.
        
        Args:
            field_name: The field to generate a suggestion for
            context: Dictionary of already filled fields
            
        Returns:
            Suggested value for the field
        """
        # Build context summary
        context_text = self._build_context(context)
        
        # Field-specific prompts
        field_prompts = {
            "product_category": f"Based on this product information, suggest a concise product category (1-3 words):\n{context_text}",
            "product_features": f"Based on this product, list 3-5 key features and functionalities:\n{context_text}",
            "product_usp": f"Based on this product, identify 2-3 unique selling points that differentiate it:\n{context_text}",
            "product_branding": f"Based on this product, suggest branding and packaging ideas:\n{context_text}",
            "target_primary": f"Based on this product, describe the primary target audience:\n{context_text}",
            "target_demographics": f"Based on this product and target audience, provide demographic details (age, gender, location, income):\n{context_text}",
            "target_psychographics": f"Based on this product and target audience, describe psychographic details (interests, lifestyle, values):\n{context_text}",
            "target_problems": f"Based on this product, what customer needs or problems does it solve?\n{context_text}",
            "competitors": f"Based on this product category, list 3-5 key competitors:\n{context_text}",
            "suggested_price": f"Based on this product and market, suggest a price or price range:\n{context_text}",
            "marketing_channels": f"Based on this product and target audience, suggest the best marketing channels:\n{context_text}",
            "tone_of_voice": f"Based on this product and target audience, suggest the brand's tone of voice and key message:\n{context_text}",
            "sales_goals": f"Based on this product and market, suggest realistic sales goals:\n{context_text}",
        }
        
        # Get the appropriate prompt or use a generic one
        prompt = field_prompts.get(
            field_name,
            f"Based on the following product information, suggest a value for '{field_name}':\n{context_text}"
        )
        
        # Add instruction for concise response
        full_prompt = f"{prompt}\n\nProvide a clear, concise, and actionable suggestion. Keep it brief and directly usable."
        
        # Call LLM
        messages = [
            {"role": "system", "content": "You are a helpful marketing assistant that provides concise, practical suggestions for product marketing plans. Keep responses brief and directly usable."},
            {"role": "user", "content": full_prompt}
        ]
        
        return self.llm.chat(messages, temperature=0.7)
    
    def _build_context(self, context: dict) -> str:
        """Build a readable context string from filled fields"""
        if not context:
            return "No information provided yet."
        
        parts = []
        
        # Product info
        if context.get('product_name'):
            parts.append(f"Product Name: {context['product_name']}")
        if context.get('product_category'):
            parts.append(f"Category: {context['product_category']}")
        if context.get('product_features'):
            parts.append(f"Features: {context['product_features']}")
        if context.get('product_usp'):
            parts.append(f"USPs: {context['product_usp']}")
        
        # Target audience
        if context.get('target_primary'):
            parts.append(f"Target Audience: {context['target_primary']}")
        if context.get('target_demographics'):
            parts.append(f"Demographics: {context['target_demographics']}")
        
        # Market info
        if context.get('competitors'):
            parts.append(f"Competitors: {context['competitors']}")
        if context.get('suggested_price'):
            parts.append(f"Price: {context['suggested_price']}")
        
        return "\n".join(parts) if parts else "No information provided yet."


# Singleton instance
field_assistant_agent = FieldAssistantAgent()
