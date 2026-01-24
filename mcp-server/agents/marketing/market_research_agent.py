"""
Market Research Agent - Collects and analyzes market, audience, and competitor information
"""
import json
from typing import Dict, List
from ..llm_client import llm_client


class MarketResearchAgent:
    """
    AI Agent that conducts market research and analysis.
    Generates: Target audience personas, SWOT analysis, competitor insights, and trend analysis.
    """
    
    def __init__(self):
        self.llm = llm_client
    
    def conduct_full_research(self, product_data: Dict) -> Dict:
        """
        Conduct comprehensive market research based on product data.
        
        Args:
            product_data: Dictionary containing product information
            
        Returns:
            Complete research report with all analysis sections
        """
        print("🔍 Starting comprehensive market research...")
        
        research_report = {
            "market_analysis": self.analyze_market(product_data),
            "target_audience": self.analyze_target_audience(product_data),
            "personas": self.create_personas(product_data),
            "competitor_analysis": self.analyze_competitors(product_data),
            "swot_analysis": self.generate_swot(product_data),
            "trends": self.identify_trends(product_data)
        }
        
        print("✅ Market research completed!")
        return research_report
    
    def analyze_market(self, product_data: Dict) -> Dict:
        """
        Analyze the market landscape for the product.
        
        Returns:
            Market size, growth potential, key players, and market dynamics
        """
        print("  📊 Analyzing market landscape...")
        
        prompt = f"""
Analyze the market for this product:

Product Name: {product_data.get('product_name', 'N/A')}
Category: {product_data.get('product_category', 'N/A')}
Features: {product_data.get('product_features', 'N/A')}
USPs: {product_data.get('product_usp', 'N/A')}
Price: {product_data.get('suggested_price', 'N/A')}

Provide a structured market analysis including:
1. Market size and growth potential
2. Market maturity stage
3. Key market segments
4. Market trends and dynamics
5. Barriers to entry
6. Opportunities and threats

Format your response as JSON with these keys: market_size, growth_potential, maturity_stage, segments, trends, barriers, opportunities, threats
"""
        
        messages = [
            {"role": "system", "content": "You are an expert market analyst. Provide detailed, data-driven insights. Always respond with valid JSON format."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.llm.chat(messages, temperature=0.6)
        return self._parse_json_response(response, {
            "market_size": "To be determined based on research",
            "growth_potential": "Moderate",
            "maturity_stage": "Growing",
            "segments": [],
            "trends": [],
            "barriers": [],
            "opportunities": [],
            "threats": []
        })
    
    def analyze_target_audience(self, product_data: Dict) -> Dict:
        """
        Analyze and segment the target audience.
        
        Returns:
            Detailed target audience analysis with segments
        """
        print("  👥 Analyzing target audience...")
        
        prompt = f"""
Analyze the target audience for this product:

Product Name: {product_data.get('product_name', 'N/A')}
Category: {product_data.get('product_category', 'N/A')}
Primary Target: {product_data.get('target_primary', 'N/A')}
Demographics: {product_data.get('target_demographics', 'N/A')}
Psychographics: {product_data.get('target_psychographics', 'N/A')}
Customer Problems: {product_data.get('target_problems', 'N/A')}

Provide a structured target audience analysis including:
1. Primary audience segment (detailed description)
2. Secondary audience segments
3. Audience size estimation
4. Key characteristics and behaviors
5. Pain points and needs
6. Purchase motivations
7. Media consumption habits

Format your response as JSON with these keys: primary_segment, secondary_segments, audience_size, characteristics, pain_points, motivations, media_habits
"""
        
        messages = [
            {"role": "system", "content": "You are an expert audience researcher. Provide detailed, actionable insights. Always respond with valid JSON format."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.llm.chat(messages, temperature=0.6)
        return self._parse_json_response(response, {
            "primary_segment": "General consumers",
            "secondary_segments": [],
            "audience_size": "To be determined",
            "characteristics": [],
            "pain_points": [],
            "motivations": [],
            "media_habits": []
        })
    
    def create_personas(self, product_data: Dict) -> List[Dict]:
        """
        Create 2-3 detailed buyer personas.
        
        Returns:
            List of persona dictionaries
        """
        print("  👤 Creating buyer personas...")
        
        prompt = f"""
Create 2-3 detailed buyer personas for this product:

Product Name: {product_data.get('product_name', 'N/A')}
Category: {product_data.get('product_category', 'N/A')}
Target Audience: {product_data.get('target_primary', 'N/A')}
Demographics: {product_data.get('target_demographics', 'N/A')}
Psychographics: {product_data.get('target_psychographics', 'N/A')}

For each persona, include:
1. Name and age
2. Job title and income level
3. Goals and aspirations
4. Challenges and pain points
5. Behaviors and preferences
6. Technology usage
7. Buying motivations
8. Preferred communication channels

Format your response as a JSON array of persona objects with these keys: name, age, job_title, income, goals, challenges, behaviors, tech_usage, buying_motivations, channels
"""
        
        messages = [
            {"role": "system", "content": "You are an expert at creating detailed, realistic buyer personas. Always respond with valid JSON format as an array."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.llm.chat(messages, temperature=0.7)
        return self._parse_json_response(response, [
            {
                "name": "Default Persona",
                "age": 35,
                "job_title": "Professional",
                "income": "Middle income",
                "goals": ["Improve quality of life"],
                "challenges": ["Limited time", "Budget constraints"],
                "behaviors": ["Online shopping", "Social media user"],
                "tech_usage": "Moderate",
                "buying_motivations": ["Quality", "Value"],
                "channels": ["Social media", "Email"]
            }
        ])
    
    def analyze_competitors(self, product_data: Dict) -> Dict:
        """
        Analyze key competitors and competitive landscape.
        
        Returns:
            Competitor analysis with strengths, weaknesses, and positioning
        """
        print("  🏢 Analyzing competitors...")
        
        prompt = f"""
Analyze the competitive landscape for this product:

Product Name: {product_data.get('product_name', 'N/A')}
Category: {product_data.get('product_category', 'N/A')}
Competitors: {product_data.get('competitors', 'N/A')}
Price: {product_data.get('suggested_price', 'N/A')}
USPs: {product_data.get('product_usp', 'N/A')}

Provide:
1. List of 3-5 main competitors with brief descriptions
2. Competitive intensity (High/Medium/Low)
3. Each competitor's strengths and weaknesses
4. Market positioning of competitors
5. Competitive gaps and opportunities
6. Differentiation strategy recommendations

Format your response as JSON with these keys: competitors (array of objects with name, description, strengths, weaknesses, positioning), competitive_intensity, gaps, differentiation_recommendations
"""
        
        messages = [
            {"role": "system", "content": "You are an expert competitive analyst. Provide strategic insights. Always respond with valid JSON format."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.llm.chat(messages, temperature=0.6)
        return self._parse_json_response(response, {
            "competitors": [],
            "competitive_intensity": "Medium",
            "gaps": [],
            "differentiation_recommendations": []
        })
    
    def generate_swot(self, product_data: Dict) -> Dict:
        """
        Generate a comprehensive SWOT analysis.
        
        Returns:
            SWOT analysis with strengths, weaknesses, opportunities, threats
        """
        print("  📋 Generating SWOT analysis...")
        
        prompt = f"""
Create a comprehensive SWOT analysis for this product:

Product Name: {product_data.get('product_name', 'N/A')}
Category: {product_data.get('product_category', 'N/A')}
Features: {product_data.get('product_features', 'N/A')}
USPs: {product_data.get('product_usp', 'N/A')}
Target Audience: {product_data.get('target_primary', 'N/A')}
Competitors: {product_data.get('competitors', 'N/A')}
Price: {product_data.get('suggested_price', 'N/A')}

Provide a detailed SWOT analysis:

STRENGTHS (Internal positive factors):
- List 4-6 key strengths

WEAKNESSES (Internal negative factors):
- List 4-6 key weaknesses

OPPORTUNITIES (External positive factors):
- List 4-6 market opportunities

THREATS (External negative factors):
- List 4-6 potential threats

Format your response as JSON with arrays for: strengths, weaknesses, opportunities, threats
"""
        
        messages = [
            {"role": "system", "content": "You are an expert strategic analyst. Provide thorough, balanced SWOT analysis. Always respond with valid JSON format."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.llm.chat(messages, temperature=0.6)
        return self._parse_json_response(response, {
            "strengths": ["Quality product"],
            "weaknesses": ["Limited brand awareness"],
            "opportunities": ["Growing market"],
            "threats": ["Strong competition"]
        })
    
    def identify_trends(self, product_data: Dict) -> Dict:
        """
        Identify relevant market trends and insights.
        
        Returns:
            Current trends, emerging trends, and implications
        """
        print("  📈 Identifying market trends...")
        
        prompt = f"""
Identify relevant market trends for this product:

Product Name: {product_data.get('product_name', 'N/A')}
Category: {product_data.get('product_category', 'N/A')}
Target Audience: {product_data.get('target_primary', 'N/A')}

Provide:
1. Current market trends (4-6 trends)
2. Emerging trends (3-4 future trends)
3. Consumer behavior trends
4. Technology trends relevant to this market
5. Implications for this product

Format your response as JSON with these keys: current_trends (array), emerging_trends (array), consumer_trends (array), technology_trends (array), implications (array)
"""
        
        messages = [
            {"role": "system", "content": "You are an expert trend analyst. Provide forward-thinking insights. Always respond with valid JSON format."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.llm.chat(messages, temperature=0.7)
        return self._parse_json_response(response, {
            "current_trends": [],
            "emerging_trends": [],
            "consumer_trends": [],
            "technology_trends": [],
            "implications": []
        })
    
    def _parse_json_response(self, response: str, fallback: any) -> any:
        """
        Parse JSON response from LLM, with fallback for malformed JSON.
        """
        try:
            # Try to find JSON in the response
            response = response.strip()
            
            # Remove markdown code blocks if present
            if response.startswith("```json"):
                response = response[7:]
            elif response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            
            response = response.strip()
            return json.loads(response)
        except json.JSONDecodeError as e:
            print(f"    ⚠️  Warning: Could not parse JSON response. Using fallback. Error: {e}")
            return fallback


# Singleton instance
market_research_agent = MarketResearchAgent()
