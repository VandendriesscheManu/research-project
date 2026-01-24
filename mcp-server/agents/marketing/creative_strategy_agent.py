"""
Creative Strategy Agent - Develops integrated marketing strategy and campaigns
"""
import json
from typing import Dict, List
from ..llm_client import llm_client


class CreativeStrategyAgent:
    """
    AI Agent that develops marketing strategy, positioning, messaging, and campaigns.
    Generates: Marketing strategy, positioning, messaging, marketing mix, and campaign ideas.
    """
    
    def __init__(self):
        self.llm = llm_client
    
    def develop_full_strategy(self, product_data: Dict, research_data: Dict) -> Dict:
        """
        Develop comprehensive marketing strategy based on product and research data.
        
        Args:
            product_data: Dictionary containing product information
            research_data: Dictionary containing market research results
            
        Returns:
            Complete strategy with all components
        """
        print("🎨 Developing marketing strategy...")
        
        strategy = {
            "executive_summary": self.create_executive_summary(product_data, research_data),
            "mission_vision_value": self.define_mission_vision_value(product_data),
            "positioning": self.create_positioning(product_data, research_data),
            "messaging": self.develop_messaging(product_data, research_data),
            "marketing_goals": self.define_marketing_goals(product_data, research_data),
            "marketing_mix": self.create_marketing_mix(product_data, research_data),
            "action_plan": self.create_action_plan(product_data, research_data),
            "budget": self.estimate_budget(product_data, research_data),
            "monitoring": self.define_monitoring_plan(product_data),
            "risks": self.identify_risks(product_data, research_data),
            "launch_strategy": self.create_launch_strategy(product_data, research_data)
        }
        
        print("✅ Marketing strategy completed!")
        return strategy
    
    def create_executive_summary(self, product_data: Dict, research_data: Dict) -> Dict:
        """
        Create executive summary for the marketing plan.
        
        Returns:
            Brief overview of product, objectives, strategy, and expected results
        """
        print("  📄 Creating executive summary...")
        
        prompt = f"""
Create a compelling executive summary for this marketing plan:

PRODUCT:
- Name: {product_data.get('product_name', 'N/A')}
- Category: {product_data.get('product_category', 'N/A')}
- USPs: {product_data.get('product_usp', 'N/A')}

MARKET INSIGHTS:
- Market Size: {research_data.get('market_analysis', {}).get('market_size', 'N/A')}
- Target Audience: {product_data.get('target_primary', 'N/A')}
- Key Opportunities: {research_data.get('swot_analysis', {}).get('opportunities', [])}

Create a concise executive summary (3-4 paragraphs) covering:
1. Product overview and value proposition
2. Market opportunity
3. Target audience
4. Key strategic approach
5. Expected outcomes

Format as JSON with keys: overview, market_opportunity, target, strategy, expected_outcomes
"""
        
        messages = [
            {"role": "system", "content": "You are an expert marketing strategist. Write clear, compelling executive summaries. Always respond with valid JSON format."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.llm.chat(messages, temperature=0.7)
        return self._parse_json_response(response, {
            "overview": "Product overview pending",
            "market_opportunity": "Market opportunity pending",
            "target": "Target audience pending",
            "strategy": "Strategy pending",
            "expected_outcomes": "Expected outcomes pending"
        })
    
    def define_mission_vision_value(self, product_data: Dict) -> Dict:
        """
        Define mission, vision, and value proposition.
        
        Returns:
            Mission statement, vision, and unique value proposition
        """
        print("  🎯 Defining mission, vision, and value proposition...")
        
        prompt = f"""
Define the mission, vision, and value proposition for this product:

Product Name: {product_data.get('product_name', 'N/A')}
Category: {product_data.get('product_category', 'N/A')}
Features: {product_data.get('product_features', 'N/A')}
USPs: {product_data.get('product_usp', 'N/A')}
Target Audience: {product_data.get('target_primary', 'N/A')}
Customer Problems: {product_data.get('target_problems', 'N/A')}

Create:
1. Mission Statement - What is the product's purpose? (1-2 sentences)
2. Vision Statement - What future does the product aspire to create? (1-2 sentences)
3. Value Proposition - Why should customers choose this product? What unique value does it deliver? (2-3 sentences)
4. Core Values - 3-5 key values that guide the brand

Format as JSON with keys: mission, vision, value_proposition, core_values (array)
"""
        
        messages = [
            {"role": "system", "content": "You are an expert brand strategist. Create inspiring, authentic statements. Always respond with valid JSON format."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.llm.chat(messages, temperature=0.7)
        return self._parse_json_response(response, {
            "mission": "To be defined",
            "vision": "To be defined",
            "value_proposition": "To be defined",
            "core_values": []
        })
    
    def create_positioning(self, product_data: Dict, research_data: Dict) -> Dict:
        """
        Develop positioning strategy.
        
        Returns:
            Positioning statement, competitive positioning, and perceptual map
        """
        print("  📍 Creating positioning strategy...")
        
        competitors = research_data.get('competitor_analysis', {}).get('competitors', [])
        competitor_names = [c.get('name', '') for c in competitors] if competitors else []
        
        prompt = f"""
Develop a positioning strategy for this product:

Product: {product_data.get('product_name', 'N/A')}
Category: {product_data.get('product_category', 'N/A')}
USPs: {product_data.get('product_usp', 'N/A')}
Target Audience: {product_data.get('target_primary', 'N/A')}
Competitors: {', '.join(competitor_names) if competitor_names else 'N/A'}
Price Point: {product_data.get('suggested_price', 'N/A')}

Create:
1. Positioning Statement - "For [target audience] who [need], [product name] is a [category] that [benefit]. Unlike [competitors], [key differentiator]."
2. Competitive Positioning - How does this product differentiate from competitors?
3. Positioning Pillars - 3-4 key attributes that define the brand position
4. Perceptual Map Axes - 2 key dimensions for positioning (e.g., Price vs Quality, Innovation vs Tradition)

Format as JSON with keys: positioning_statement, competitive_positioning, positioning_pillars (array), perceptual_map_axes (object with x_axis and y_axis)
"""
        
        messages = [
            {"role": "system", "content": "You are an expert positioning strategist. Create clear, differentiated positioning. Always respond with valid JSON format."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.llm.chat(messages, temperature=0.7)
        return self._parse_json_response(response, {
            "positioning_statement": "Positioning to be defined",
            "competitive_positioning": "To be defined",
            "positioning_pillars": [],
            "perceptual_map_axes": {"x_axis": "Price", "y_axis": "Quality"}
        })
    
    def develop_messaging(self, product_data: Dict, research_data: Dict) -> Dict:
        """
        Develop messaging strategy and key messages.
        
        Returns:
            Tone of voice, key messages, messaging pillars, and tagline
        """
        print("  💬 Developing messaging strategy...")
        
        prompt = f"""
Develop a messaging strategy for this product:

Product: {product_data.get('product_name', 'N/A')}
Category: {product_data.get('product_category', 'N/A')}
USPs: {product_data.get('product_usp', 'N/A')}
Target Audience: {product_data.get('target_primary', 'N/A')}
Brand Tone: {product_data.get('tone_of_voice', 'N/A')}

Create:
1. Brand Tone of Voice - Describe the communication style (3-4 adjectives with brief explanations)
2. Key Messages - 3-4 core messages that communicate value
3. Messaging Pillars - 3-4 themes that support the positioning
4. Tagline Options - 3 creative tagline options
5. Value Propositions by Audience Segment - Tailored messages for different segments

Format as JSON with keys: tone_of_voice (object), key_messages (array), messaging_pillars (array), tagline_options (array), segment_messages (object)
"""
        
        messages = [
            {"role": "system", "content": "You are an expert brand messaging strategist. Create compelling, consistent messaging. Always respond with valid JSON format."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.llm.chat(messages, temperature=0.8)
        return self._parse_json_response(response, {
            "tone_of_voice": {},
            "key_messages": [],
            "messaging_pillars": [],
            "tagline_options": [],
            "segment_messages": {}
        })
    
    def define_marketing_goals(self, product_data: Dict, research_data: Dict) -> Dict:
        """
        Define SMART marketing goals and KPIs.
        
        Returns:
            Marketing objectives and key performance indicators
        """
        print("  🎯 Defining marketing goals and KPIs...")
        
        prompt = f"""
Define SMART marketing goals and KPIs for this product:

Product: {product_data.get('product_name', 'N/A')}
Category: {product_data.get('product_category', 'N/A')}
Sales Goals: {product_data.get('sales_goals', 'N/A')}
Target Audience Size: {research_data.get('target_audience', {}).get('audience_size', 'N/A')}

Create:
1. Primary Goals - 3-4 SMART goals (Specific, Measurable, Achievable, Relevant, Time-bound)
   Examples: Brand awareness, lead generation, sales targets, market share
2. KPIs for Each Goal - Specific metrics to track success
3. Short-term Goals (0-6 months)
4. Long-term Goals (6-12 months)
5. Success Criteria - What defines success for this launch?

Format as JSON with keys: primary_goals (array of objects with goal and kpis), short_term_goals (array), long_term_goals (array), success_criteria (array)
"""
        
        messages = [
            {"role": "system", "content": "You are an expert marketing strategist. Create realistic, measurable goals. Always respond with valid JSON format."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.llm.chat(messages, temperature=0.6)
        return self._parse_json_response(response, {
            "primary_goals": [],
            "short_term_goals": [],
            "long_term_goals": [],
            "success_criteria": []
        })
    
    def create_marketing_mix(self, product_data: Dict, research_data: Dict) -> Dict:
        """
        Develop the marketing mix (7Ps).
        
        Returns:
            Product, Price, Place, Promotion, People, Process, Physical Evidence strategies
        """
        print("  🛍️ Creating marketing mix (7Ps)...")
        
        prompt = f"""
Develop a comprehensive marketing mix (7Ps) for this product:

Product: {product_data.get('product_name', 'N/A')}
Features: {product_data.get('product_features', 'N/A')}
Price: {product_data.get('suggested_price', 'N/A')}
Target Audience: {product_data.get('target_primary', 'N/A')}
Channels: {product_data.get('marketing_channels', 'N/A')}

Create strategies for:
1. PRODUCT - Product strategy, features, packaging, branding
2. PRICE - Pricing strategy, discounts, payment terms
3. PLACE - Distribution channels, availability, logistics
4. PROMOTION - Communication channels, campaigns, content strategy
5. PEOPLE - Team, customer service, brand ambassadors
6. PROCESS - Customer journey, purchase process, delivery
7. PHYSICAL EVIDENCE - Website, packaging, retail environment, brand touchpoints

Format as JSON with keys: product, price, place, promotion, people, process, physical_evidence (each as an object with strategy and details)
"""
        
        messages = [
            {"role": "system", "content": "You are an expert marketing mix strategist. Create comprehensive, actionable strategies. Always respond with valid JSON format."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.llm.chat(messages, temperature=0.7)
        return self._parse_json_response(response, {
            "product": {"strategy": "", "details": []},
            "price": {"strategy": "", "details": []},
            "place": {"strategy": "", "details": []},
            "promotion": {"strategy": "", "details": []},
            "people": {"strategy": "", "details": []},
            "process": {"strategy": "", "details": []},
            "physical_evidence": {"strategy": "", "details": []}
        })
    
    def create_action_plan(self, product_data: Dict, research_data: Dict) -> Dict:
        """
        Create tactical action plan with timeline.
        
        Returns:
            Detailed action plan with phases, activities, and timeline
        """
        print("  📅 Creating action plan and timeline...")
        
        prompt = f"""
Create a detailed action plan for launching this product:

Product: {product_data.get('product_name', 'N/A')}
Marketing Channels: {product_data.get('marketing_channels', 'N/A')}

Create a phased action plan:

PHASE 1: PRE-LAUNCH (Months -3 to 0)
- List 6-8 key activities with timeline and responsible party

PHASE 2: LAUNCH (Month 0-1)
- List 6-8 key launch activities with timeline

PHASE 3: POST-LAUNCH (Months 1-6)
- List 6-8 ongoing activities and optimization efforts

For each activity include:
- Activity name
- Description
- Timeline (specific weeks/months)
- Responsible party/team
- Dependencies
- Expected outcome

Format as JSON with keys: pre_launch (array), launch (array), post_launch (array)
Each activity should be an object with: activity, description, timeline, responsible, dependencies, expected_outcome
"""
        
        messages = [
            {"role": "system", "content": "You are an expert marketing project manager. Create detailed, actionable plans. Always respond with valid JSON format."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.llm.chat(messages, temperature=0.6)
        return self._parse_json_response(response, {
            "pre_launch": [],
            "launch": [],
            "post_launch": []
        })
    
    def estimate_budget(self, product_data: Dict, research_data: Dict) -> Dict:
        """
        Estimate marketing budget and resource allocation.
        
        Returns:
            Budget breakdown by category and ROI projections
        """
        print("  💰 Estimating budget and resources...")
        
        prompt = f"""
Create a marketing budget estimate for this product:

Product: {product_data.get('product_name', 'N/A')}
Price: {product_data.get('suggested_price', 'N/A')}
Channels: {product_data.get('marketing_channels', 'N/A')}
Sales Goals: {product_data.get('sales_goals', 'N/A')}

Provide:
1. Total Marketing Budget Recommendation (as % of projected revenue)
2. Budget Breakdown by Category:
   - Digital Marketing (SEO, SEM, Social Media Ads)
   - Content Creation (Video, Graphics, Copywriting)
   - PR & Influencer Marketing
   - Events & Sponsorships
   - Tools & Technology
   - Personnel/Agency Costs
3. Budget Allocation by Phase (Pre-launch, Launch, Post-launch)
4. ROI Projections
5. Resource Requirements (team members, tools, agencies)

Format as JSON with keys: total_budget, budget_breakdown (object), phase_allocation (object), roi_projections (object), resource_requirements (array)
"""
        
        messages = [
            {"role": "system", "content": "You are an expert marketing budget planner. Provide realistic estimates. Always respond with valid JSON format."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.llm.chat(messages, temperature=0.6)
        return self._parse_json_response(response, {
            "total_budget": "To be determined",
            "budget_breakdown": {},
            "phase_allocation": {},
            "roi_projections": {},
            "resource_requirements": []
        })
    
    def define_monitoring_plan(self, product_data: Dict) -> Dict:
        """
        Define monitoring and evaluation framework.
        
        Returns:
            Metrics, tracking methods, and evaluation schedule
        """
        print("  📊 Defining monitoring and evaluation plan...")
        
        prompt = f"""
Create a monitoring and evaluation plan for this marketing campaign:

Product: {product_data.get('product_name', 'N/A')}

Define:
1. Key Metrics to Track:
   - Awareness metrics
   - Engagement metrics
   - Conversion metrics
   - Retention metrics
2. Tracking Tools and Methods
3. Reporting Schedule (daily, weekly, monthly)
4. Dashboard Requirements
5. Review Milestones (when to evaluate and adjust strategy)
6. Success Thresholds (when to scale up or pivot)

Format as JSON with keys: key_metrics (object with categories), tracking_tools (array), reporting_schedule (object), dashboard_requirements (array), review_milestones (array), success_thresholds (object)
"""
        
        messages = [
            {"role": "system", "content": "You are an expert marketing analyst. Create comprehensive tracking plans. Always respond with valid JSON format."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.llm.chat(messages, temperature=0.6)
        return self._parse_json_response(response, {
            "key_metrics": {},
            "tracking_tools": [],
            "reporting_schedule": {},
            "dashboard_requirements": [],
            "review_milestones": [],
            "success_thresholds": {}
        })
    
    def identify_risks(self, product_data: Dict, research_data: Dict) -> Dict:
        """
        Identify risks and mitigation strategies.
        
        Returns:
            Risk assessment and mitigation plans
        """
        print("  ⚠️ Identifying risks and mitigation strategies...")
        
        threats = research_data.get('swot_analysis', {}).get('threats', [])
        
        prompt = f"""
Identify risks and mitigation strategies for this product launch:

Product: {product_data.get('product_name', 'N/A')}
Category: {product_data.get('product_category', 'N/A')}
Market Threats: {', '.join(threats) if threats else 'N/A'}

Identify 6-8 key risks in these categories:
1. Market Risks (competition, market changes)
2. Operational Risks (supply chain, technical issues)
3. Financial Risks (budget overruns, poor ROI)
4. Reputational Risks (negative feedback, PR issues)

For each risk provide:
- Risk description
- Probability (High/Medium/Low)
- Impact (High/Medium/Low)
- Mitigation strategy
- Contingency plan

Format as JSON with key: risks (array of objects with: category, description, probability, impact, mitigation, contingency)
"""
        
        messages = [
            {"role": "system", "content": "You are an expert risk analyst. Provide thorough risk assessments. Always respond with valid JSON format."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.llm.chat(messages, temperature=0.6)
        return self._parse_json_response(response, {
            "risks": []
        })
    
    def create_launch_strategy(self, product_data: Dict, research_data: Dict) -> Dict:
        """
        Create comprehensive launch strategy.
        
        Returns:
            Launch strategy with phases, tactics, and timeline
        """
        print("  🚀 Creating launch strategy...")
        
        prompt = f"""
Create a comprehensive product launch strategy:

Product: {product_data.get('product_name', 'N/A')}
Category: {product_data.get('product_category', 'N/A')}
Target Audience: {product_data.get('target_primary', 'N/A')}
Channels: {product_data.get('marketing_channels', 'N/A')}

Create:
1. Launch Approach - Big bang vs phased rollout? Why?
2. Pre-Launch Phase:
   - Teaser campaigns
   - Beta testing/Early access
   - PR and media outreach
   - Influencer partnerships
3. Launch Phase:
   - Launch event/announcement
   - Initial promotions and offers
   - Media coverage tactics
   - Social media strategy
4. Post-Launch Phase:
   - Customer feedback collection
   - Optimization and iteration
   - Expansion strategy
5. Adoption Strategy - How to drive adoption and overcome barriers
6. Launch Timeline - Detailed week-by-week plan

Format as JSON with keys: launch_approach, pre_launch (object), launch_phase (object), post_launch_phase (object), adoption_strategy (object), timeline (array)
"""
        
        messages = [
            {"role": "system", "content": "You are an expert product launch strategist. Create compelling launch plans. Always respond with valid JSON format."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.llm.chat(messages, temperature=0.7)
        return self._parse_json_response(response, {
            "launch_approach": "To be determined",
            "pre_launch": {},
            "launch_phase": {},
            "post_launch_phase": {},
            "adoption_strategy": {},
            "timeline": []
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
creative_strategy_agent = CreativeStrategyAgent()
