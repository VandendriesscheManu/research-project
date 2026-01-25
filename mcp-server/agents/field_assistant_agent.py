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
        
        # Field-specific prompts - Direct output format
        field_prompts = {
            "product_category": f"Product category (1-3 words):\n{context_text}",
            "product_features": f"List 3-5 key product features:\n{context_text}",
            "product_usp": f"List 2-3 unique selling points:\n{context_text}",
            "product_branding": f"Branding and packaging ideas:\n{context_text}",
            "target_primary": f"Primary target audience:\n{context_text}",
            "target_demographics": f"Demographics (age, gender, location, income):\n{context_text}",
            "target_psychographics": f"Psychographics (interests, lifestyle, values):\n{context_text}",
            "target_problems": f"Customer needs and problems this solves:\n{context_text}",
            "competitors": f"Key competitors (3-5):\n{context_text}",
            "suggested_price": f"Suggested price or price range:\n{context_text}",
            "marketing_channels": f"Best marketing channels:\n{context_text}",
            "tone_of_voice": f"Brand tone of voice and key message:\n{context_text}",
            "sales_goals": f"Realistic sales goals:\n{context_text}",
            "market_share_goals": f"Market share goals:\n{context_text}",
            "brand_awareness_goals": f"Brand awareness goals:\n{context_text}",
            "kpis": f"Key metrics to track (KPIs):\n{context_text}",
        }
        
        # Get the appropriate prompt or use a generic one
        prompt = field_prompts.get(
            field_name,
            f"Suggestion for {field_name.replace('_', ' ')}:\n{context_text}"
        )
        
        # Add instruction for direct response
        full_prompt = f"{prompt}\n\nProvide ONLY the direct answer without any introductory phrases like 'Based on...' or 'I suggest...'. Write as if filling the field directly."
        
        # Call LLM
        messages = [
            {"role": "system", "content": "You are a marketing assistant. Provide direct, concise content that can be used immediately in the field. Never use phrases like 'Based on...', 'I suggest...', 'Consider...', 'For this field...', or any other introductory language. Write as if you are filling the field yourself with the actual content."},
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
