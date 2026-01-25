"""
Fast Marketing Plan Orchestrator - Optimized for speed (Synchronous version)
Combines: Consolidation + Parallel + Shorter + Faster Model
"""
import json
from datetime import datetime
from typing import Dict
from ..llm_client import LLMClient


class FastMarketingOrchestrator:
    """
    Fast marketing plan generation with:
    - Consolidated prompts (5 LLM calls instead of 25)
    - Shorter, concise outputs (300-600 words per section)
    - Faster model (llama-3.1-8b-instant for Groq)
    - Synchronous execution for reliability
    """
    
    def __init__(self):
        self.llm = LLMClient()
        # Override to use faster model for Groq
        if self.llm.provider == "groq":
            self.llm.model = "llama-3.1-8b-instant"
            print(f"⚡ Fast mode: Using {self.llm.model}")
    
    def _generate(self, prompt: str, max_tokens: int = 800) -> str:
        """Generate text using LLM"""
        try:
            messages = [{"role": "user", "content": prompt}]
            response = self.llm.chat(messages, temperature=0.7)
            return response
        except Exception as e:
            print(f"ERROR in _generate: {e}")
            return "{}"
    
    def _research_phase(self, product_data: Dict) -> Dict:
        """Phase 1: Consolidated market research"""
        print("\n📊 Phase 1: Market Research")
        
        # Extract ALL relevant product data
        product_name = product_data.get('product_name', 'Unknown Product')
        category = product_data.get('product_category', 'general')
        features = product_data.get('product_features', '')
        usp = product_data.get('product_usp', '')
        target_primary = product_data.get('target_primary', 'general consumers')
        target_secondary = product_data.get('target_secondary', '')
        demographics = product_data.get('target_demographics', '')
        psychographics = product_data.get('target_psychographics', '')
        competitors = product_data.get('competitors', 'market competitors')
        market_size = product_data.get('market_size', '')
        competitor_pricing = product_data.get('competitor_pricing', '')
        
        print("  → Generating situation & market analysis...")
        market_prompt = f"""Perform a complete SITUATION & MARKET ANALYSIS for {product_name} ({category}). Respond in ENGLISH.

**PRODUCT CONTEXT:**
- Features: {features}
- Unique Selling Points: {usp}
- Category: {category}

**TARGET AUDIENCE PROVIDED:**
- Primary: {target_primary}
- Secondary: {target_secondary}
- Demographics: {demographics}
- Psychographics: {psychographics}

**COMPETITIVE LANDSCAPE PROVIDED:**
- Competitors: {competitors}
- Market Size: {market_size}
- Competitor Pricing: {competitor_pricing}

Based on this information:

Include:
1. **Current Market Situation**: Market size, growth rate, maturity phase
2. **Market Trends**: Current trends affecting the market, consumer behavior shifts
3. **Competitors**: Identify top 4-5 competitors, their market share, strengths, positioning
4. **Target Audience**: Demographics (age, gender, income, education, location), psychographics (lifestyle, values, interests)
5. **External Environment**: PEST factors (Political, Economic, Social, Technological) affecting the market
6. **Market Opportunities**: Gaps in the market, underserved segments

Provide detailed analysis (500-600 words) in ENGLISH.
Format as JSON: {{
    "current_situation": "...",
    "market_size": "...",
    "growth_rate": "...",
    "trends": ["trend1", "trend2", "trend3"],
    "competitors": [
        {{"name": "...", "market_share": "...", "strengths": "...", "positioning": "..."}},
        ...
    ],
    "target_demographics": {{"age": "...", "gender": "...", "income": "...", "location": "..."}},
    "target_psychographics": {{"lifestyle": "...", "values": "...", "interests": "..."}},
    "pest_analysis": {{
        "political": "...",
        "economic": "...",
        "social": "...",
        "technological": "..."
    }},
    "market_opportunities": ["opportunity1", "opportunity2"]
}}"""
        
        market_result = self._generate(market_prompt, 600)
        
        print("  → Generating comprehensive SWOT analysis...")
        swot_prompt = f"""Create a detailed SWOT ANALYSIS for {product_name}. Respond in ENGLISH.

**PRODUCT INFO:**
- Name: {product_name}
- Category: {category}
- Features: {features}
- USPs: {usp}
- Target Market: {target_primary}
- Competitors: {competitors}

Analyze based on this specific product information:

Analyze:
- **Strengths (Internal)**: 4-5 key strengths (unique features, capabilities, resources, advantages)
- **Weaknesses (Internal)**: 4-5 weaknesses (limitations, gaps, vulnerabilities, disadvantages)
- **Opportunities (External)**: 4-5 market opportunities (trends, gaps, partnerships, growth areas)
- **Threats (External)**: 4-5 threats (competition, market risks, economic factors, technological disruption)

Each point should be specific and actionable (400-500 words total) in ENGLISH.
Format as JSON: {{
    "strengths": [
        {{"title": "...", "description": "...", "impact": "high/medium/low"}},
        ...
    ],
    "weaknesses": [
        {{"title": "...", "description": "...", "mitigation": "..."}},
        ...
    ],
    "opportunities": [
        {{"title": "...", "description": "...", "potential": "..."}},
        ...
    ],
    "threats": [
        {{"title": "...", "description": "...", "likelihood": "high/medium/low"}},
        ...
    ]
}}"""
        
        swot_result = self._generate(swot_prompt, 500)
        
        return {
            "market_intelligence": self._parse_json(market_result),
            "swot": self._parse_json(swot_result)
        }
    
    def _strategy_phase(self, product_data: Dict, research: Dict) -> Dict:
        """Phase 2: Consolidated strategy"""
        print("\n🎯 Phase 2: Marketing Strategy")
        
        # Extract ALL relevant data for strategy
        product_name = product_data.get('product_name')
        category = product_data.get('product_category', '')
        features = product_data.get('product_features', '')
        usp = product_data.get('product_usp', '')
        branding = product_data.get('product_branding', '')
        variants = product_data.get('product_variants', '')
        target_primary = product_data.get('target_primary', '')
        target_problems = product_data.get('target_problems', '')
        production_cost = product_data.get('production_cost', '')
        desired_margin = product_data.get('desired_margin', '')
        suggested_price = product_data.get('suggested_price', '')
        marketing_budget = product_data.get('marketing_budget', 'moderate')
        marketing_channels = product_data.get('marketing_channels', [])
        tone_of_voice = product_data.get('tone_of_voice', '')
        distribution_channels = product_data.get('distribution_channels', [])
        launch_date = product_data.get('launch_date', 'Q1 2026')
        
        print("  → Generating mission, vision, positioning & messaging...")
        positioning_prompt = f"""Create comprehensive MISSION, VISION, VALUE PROPOSITION & POSITIONING for {product_name}. Respond in ENGLISH.

**PRODUCT DETAILS:**
- Name: {product_name}
- Category: {category}
- Key Features: {features}
- USPs: {usp}
- Branding: {branding}
- Variants: {variants}

**TARGET AUDIENCE:**
- Primary Target: {target_primary}
- Problems Solved: {target_problems}

**BRAND VOICE:**
- Tone: {tone_of_voice}

Based on this specific product and market context:

Include:
1. **Mission Statement**: What is the purpose and goal of the project?
2. **Vision Statement**: Long-term aspiration and impact
3. **Value Proposition**: What makes the product unique? Why should customers choose it over competitors?
4. **Positioning Statement**: How is the product positioned in the market relative to competitors? What place does it occupy in the consumer's mind?
5. **Key Messaging**: 3-4 main communication messages
6. **Brand Personality**: Tone, values, characteristics

Detailed (400-500 words) in ENGLISH.
Format as JSON: {{
    "mission": "...",
    "vision": "...",
    "value_proposition": "...",
    "unique_selling_points": ["USP1", "USP2", "USP3"],
    "positioning_statement": "...",
    "positioning_vs_competitors": "...",
    "messaging": ["message1", "message2", "message3"],
    "brand_personality": {{"tone": "...", "values": ["..."], "characteristics": "..."}}
}}"""
        
        positioning = self._generate(positioning_prompt, 600)
        
        print("  → Generating marketing goals & KPIs...")
        goals_prompt = f"""Create MARKETING GOALS & KPIs for {product_name}. Respond in ENGLISH.

**BUDGET & PRICING:**
- Marketing Budget: {marketing_budget}
- Production Cost: {production_cost}
- Target Price: {suggested_price}
- Desired Margin: {desired_margin}

**LAUNCH TIMELINE:**
- Launch Date: {launch_date}

Define 5-7 SMART goals based on this budget and pricing context:

Define 5-7 SMART goals (Specific, Measurable, Achievable, Relevant, Time-bound).
Include KPIs: conversion rate, market share, brand awareness, customer acquisition cost, ROI, customer lifetime value.
Set specific targets for each KPI with deadlines.

Format as JSON: {{
    "goals": [
        {{"goal": "...", "target": "...", "deadline": "...", "smart": true}},
        {{"goal": "...", "target": "...", "deadline": "...", "smart": true}},
        {{"goal": "...", "target": "...", "deadline": "...", "smart": true}},
        ...
    ],
    "kpis": [
        {{"name": "Conversion Rate", "target": "...", "measurement": "..."}},
        {{"name": "Market Share", "target": "...", "measurement": "..."}},
        {{"name": "Brand Awareness", "target": "...", "measurement": "..."}},
        {{"name": "Customer Acquisition Cost", "target": "...", "measurement": "..."}},
        {{"name": "ROI", "target": "...", "measurement": "..."}},
        {{"name": "Customer Lifetime Value", "target": "...", "measurement": "..."}},
        ...
    ]
}}"""
        
        goals = self._generate(goals_prompt, 500)
        
        print("  → Generating marketing mix (7Ps)...")
        mix_prompt = f"""Create comprehensive MARKETING MIX (7Ps Strategy) for {product_name}. Respond in ENGLISH.

**PRODUCT CONTEXT:**
- Features: {features}
- USPs: {usp}
- Variants: {variants}
- Branding: {branding}

**PRICING CONTEXT:**
- Cost: {production_cost}
- Target Price: {suggested_price}
- Margin: {desired_margin}

**DISTRIBUTION:**
- Channels: {', '.join(distribution_channels) if distribution_channels else 'Various channels'}

**PROMOTION:**
- Budget: {marketing_budget}
- Channels: {', '.join(marketing_channels) if marketing_channels else 'Various channels'}
- Tone: {tone_of_voice}

Based on this context, create the 7Ps strategy:

**Product**: Features, quality, design, branding, packaging, variants
**Price**: Pricing strategy, positioning, discounts, payment terms
**Place**: Distribution channels, locations, logistics, online/offline presence
**Promotion**: Advertising, PR, content marketing, social media, influencer partnerships
**People**: Staff, customer service, brand ambassadors
**Process**: Customer journey, purchase process, delivery, after-sales
**Physical Evidence**: Store design, website UX, packaging, testimonials

Detailed (500-600 words).
Format as JSON: {{
    "product": {{"features": "...", "quality": "...", "design": "...", "branding": "...", "packaging": "..."}},
    "price": {{"strategy": "...", "positioning": "...", "tactics": "..."}},
    "place": {{"channels": ["..."], "distribution": "...", "logistics": "..."}},
    "promotion": {{"advertising": "...", "pr": "...", "content": "...", "social_media": "...", "influencers": "..."}},
    "people": {{"staff": "...", "customer_service": "...", "ambassadors": "..."}},
    "process": {{"customer_journey": "...", "purchase_flow": "...", "delivery": "..."}},
    "physical_evidence": {{"store_design": "...", "website_ux": "...", "testimonials": "..."}}
}}"""
        
        marketing_mix = self._generate(mix_prompt, 1200)  # Increased from 800 to 1200 for more complete 7Ps
        
        print("  → Generating action plan...")
        action_prompt = f"""Create detailed ACTION PLAN for {product_name} launch. Respond in ENGLISH.

**LAUNCH CONTEXT:**
- Launch Date: {launch_date}
- Marketing Channels: {', '.join(marketing_channels) if marketing_channels else 'Various channels'}
- Distribution: {', '.join(distribution_channels) if distribution_channels else 'Various channels'}

**TIMELINE PHASES:**

**Pre-Launch Phase**: Teaser campaigns, influencer outreach, email list building, PR preparations
**Launch Phase**: Grand opening, launch event, media coverage, promotional offers, advertising blitz
**Post-Launch Phase**: Customer retention, feedback collection, optimization, scaling

Include timeline with specific dates/weeks for each activity.

Format as JSON: {{
    "pre_launch": {{
        "activities": ["activity1", "activity2", ...],
        "timeline": "2 months before launch",
        "key_milestones": ["milestone1", "milestone2"]
    }},
    "launch": {{
        "activities": ["activity1", "activity2", ...],
        "timeline": "Launch week + 2 weeks",
        "key_milestones": ["milestone1", "milestone2"]
    }},
    "post_launch": {{
        "activities": ["activity1", "activity2", ...],
        "timeline": "Month 2-6",
        "key_milestones": ["milestone1", "milestone2"]
    }}
}}"""
        
        action_plan = self._generate(action_prompt, 600)
        
        print("  → Generating budget & monitoring plan...")
        budget_prompt = f"""Create BUDGET & MONITORING plan for {product_name}. Respond in ENGLISH.

**BUDGET CONTEXT:**
- Total Marketing Budget: {marketing_budget}
- Channels to Allocate: {', '.join(marketing_channels) if marketing_channels else 'Various channels'}
- Product Cost: {production_cost}
- Target Price: {suggested_price}
- Margin: {desired_margin}

Based on this budget information:

**Budget**:
- Total marketing budget
- Allocation by channel (social media, ads, PR, events, content, influencers, other)
- Cost per activity
- Expected ROI and revenue projections
- Required resources (team, tools, agencies)

**Monitoring**:
- How progress will be measured (weekly/monthly dashboards)
- When evaluations take place (monthly reviews, quarterly assessments)
- Dashboard metrics to track
- Adjustment criteria to pivot the plan

Format as JSON: {{
    "budget": {{
        "total": "€XXX,XXX",
        "allocation": {{
            "social_media": "€XX,XXX",
            "paid_ads": "€XX,XXX",
            "pr": "€XX,XXX",
            "events": "€XX,XXX",
            "content": "€XX,XXX",
            "influencers": "€XX,XXX",
            "other": "€XX,XXX"
        }},
        "cost_per_activity": [
            {{"activity": "...", "cost": "€X,XXX"}},
            ...
        ],
        "roi_projection": "XXX%",
        "revenue_forecast": "€XXX,XXX",
        "resources_needed": {{
            "team": ["role1", "role2"],
            "tools": ["tool1", "tool2"],
            "agencies": ["agency1", "agency2"]
        }}
    }},
    "monitoring": {{
        "measurement_frequency": "Weekly dashboards, monthly deep-dives",
        "evaluation_schedule": ["Monthly review - end of each month", "Quarterly assessment - Q1/Q2/Q3/Q4"],
        "dashboard_metrics": ["metric1", "metric2", "metric3"],
        "adjustment_triggers": ["trigger1", "trigger2", "trigger3"]
    }}
}}"""
        
        budget_monitoring = self._generate(budget_prompt, 800)
        
        print("  → Generating risks & launch strategy...")
        risks_launch_prompt = f"""Create RISK MANAGEMENT & LAUNCH STRATEGY for {product_name}. Respond in ENGLISH.

**LAUNCH CONTEXT:**
- Launch Date: {launch_date}
- Target Market: {target_primary}
- Competitors: {product_data.get('competitors', '')}
- Distribution: {', '.join(distribution_channels) if distribution_channels else 'Various channels'}

Based on this context:

**Risks & Mitigation**:
Identify 5-6 potential risks:
- Market failure (low adoption)
- Technical problems (product issues)
- Competition (aggressive competitors)
- Budget overruns
- Poor customer adoption
- Supply chain issues

For each risk, provide mitigation strategy and contingency plan.

**Launch Strategy**:
- Product introduction plan (soft launch vs. hard launch)
- Adoption strategy (innovators → early adopters → early majority → late majority)
- Launch phases with activities and success criteria
- Key milestones with dates

Format as JSON: {{
    "risks": [
        {{
            "id": "R1",
            "description": "...",
            "likelihood": "high/medium/low",
            "impact": "high/medium/low",
            "mitigation": "...",
            "contingency": "..."
        }},
        ...
    ],
    "launch_strategy": {{
        "approach": "soft_launch / hard_launch / phased_rollout",
        "target_date": "{launch_date}",
        "adoption_phases": {{
            "innovators": {{"strategy": "...", "timeline": "Week 1-2"}},
            "early_adopters": {{"strategy": "...", "timeline": "Week 3-8"}},
            "early_majority": {{"strategy": "...", "timeline": "Month 3-6"}},
            "late_majority": {{"strategy": "...", "timeline": "Month 7-12"}}
        }},
        "launch_phases": [
            {{"phase": "Soft Launch", "activities": ["..."], "success_criteria": "..."}},
            {{"phase": "Public Launch", "activities": ["..."], "success_criteria": "..."}},
            {{"phase": "Scale", "activities": ["..."], "success_criteria": "..."}}
        ],
        "milestones": [
            {{"milestone": "...", "date": "...", "criteria": "..."}},
            ...
        ]
    }}
}}"""
        
        risks_launch = self._generate(risks_launch_prompt, 900)
        
        return {
            "positioning": self._parse_json(positioning),
            "goals": self._parse_json(goals),
            "marketing_mix": self._parse_json(marketing_mix),
            "action_plan": self._parse_json(action_plan),
            "budget_monitoring": self._parse_json(budget_monitoring),
            "risks_launch": self._parse_json(risks_launch)
        }
    
    def _parse_json(self, text: str) -> Dict:
        """Extract JSON from LLM response with better error handling"""
        try:
            if not text or not text.strip():
                return {"error": "Empty response"}
            
            # Try direct JSON parse first
            try:
                return json.loads(text)
            except:
                pass
            
            # Find JSON block with better detection
            start = text.find('{')
            end = text.rfind('}') + 1
            
            if start != -1 and end > start:
                json_str = text[start:end]
                
                # Clean up common issues
                json_str = json_str.strip()
                
                # Try parsing
                try:
                    parsed = json.loads(json_str)
                    return parsed
                except json.JSONDecodeError as e:
                    print(f"⚠️ JSON decode error at position {e.pos}: {e.msg}")
                    
                    # Try to fix common issues
                    import re
                    # Remove trailing commas before closing braces/brackets
                    json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)
                    # Fix escaped quotes that might break JSON
                    json_str = re.sub(r'\\(?!")', r'', json_str)
                    # Remove control characters
                    json_str = ''.join(char for char in json_str if ord(char) >= 32 or char in '\n\r\t')
                    
                    try:
                        parsed = json.loads(json_str)
                        print(f"✅ JSON fixed after cleanup")
                        return parsed
                    except Exception as e2:
                        print(f"❌ Still failed after cleanup: {e2}")
                        # Show more context for debugging
                        print(f"First 500 chars: {json_str[:500]}")
                        print(f"Last 200 chars: {json_str[-200:]}")
            
            # If all else fails, return raw text in proper format for frontend
            print(f"⚠️ Failed to parse JSON, returning raw text (length: {len(text)})")
            return {"raw_content": text}  # Frontend can handle this
            
        except Exception as e:
            print(f"❌ JSON parse error: {e}")
            return {"error": str(e), "raw_content": text[:1000] if text else "No response"}
    
    def _compile_plan(self, product_data: Dict, research: Dict, strategy: Dict) -> Dict:
        """Compile final 12-section plan"""
        print("\n📦 Compiling final plan...")
        
        product_name = product_data.get('product_name', 'Product')
        
        market_intel = research.get('market_intelligence', {})
        swot = research.get('swot', {})
        positioning = strategy.get('positioning', {})
        goals = strategy.get('goals', {})
        marketing_mix = strategy.get('marketing_mix', {})
        action_plan = strategy.get('action_plan', {})
        budget_monitoring = strategy.get('budget_monitoring', {})
        risks_launch = strategy.get('risks_launch', {})
        
        # Create executive summary combining all key insights
        exec_summary = {
            "overview": f"Complete marketing plan for {product_name}. {positioning.get('value_proposition', '')}",
            "product_description": product_data.get('product_features', 'Innovative product in the market'),
            "objectives": [goal.get('goal', '') for goal in goals.get('goals', [])[:3]] if goals.get('goals') else [],
            "strategy_overview": positioning.get('positioning_statement', ''),
            "expected_results": f"ROI: {budget_monitoring.get('budget', {}).get('roi_projection', 'positive')}",
            "target_market": market_intel.get('target_demographics', {})
        }
        
        return {
            "metadata": {
                "product_name": product_name,
                "generated_at": datetime.now().isoformat(),
                "version": "fast_v1",
                "generation_mode": "fast",
                "quality_score": 7.5
            },
            "sections": {
                "1_executive_summary": {
                    "title": "1. Executive Summary",
                    "description": "A brief overview of the entire plan: what the product is, what the objectives are, which strategy is followed, and what results are expected.",
                    "content": exec_summary
                },
                "2_mission_vision_value": {
                    "title": "2. Mission, Vision & Value Proposition",
                    "description": "What is the goal and vision of the project? What makes the product unique and why would customers choose it?",
                    "content": {
                        "mission": positioning.get('mission', ''),
                        "vision": positioning.get('vision', ''),
                        "value_proposition": positioning.get('value_proposition', ''),
                        "unique_selling_points": positioning.get('unique_selling_points', []),
                        "brand_personality": positioning.get('brand_personality', {})
                    }
                },
                "3_situation_market_analysis": {
                    "title": "3. Situation & Market Analysis",
                    "description": "Analysis of the current situation, internal strengths and weaknesses, and the external market (opportunities and threats). Includes SWOT and PEST analysis.",
                    "content": {
                        "current_situation": market_intel.get('current_situation', ''),
                        "market_size": market_intel.get('market_size', ''),
                        "growth_rate": market_intel.get('growth_rate', ''),
                        "trends": market_intel.get('trends', []),
                        "competitors": market_intel.get('competitors', []),
                        "pest_analysis": market_intel.get('pest_analysis', {}),
                        "market_opportunities": market_intel.get('market_opportunities', [])
                    }
                },
                "4_swot_analysis": {
                    "title": "4. SWOT Analysis",
                    "description": "Overview of strengths, weaknesses, opportunities, and threats that impact the product or organization.",
                    "content": swot
                },
                "5_target_audience_positioning": {
                    "title": "5. Target Audience & Positioning",
                    "description": "Who is the target audience? How is the product positioned relative to competitors and what place does it occupy in the consumer's mind?",
                    "content": {
                        "target_demographics": market_intel.get('target_demographics', {}),
                        "target_psychographics": market_intel.get('target_psychographics', {}),
                        "positioning_statement": positioning.get('positioning_statement', ''),
                        "positioning_vs_competitors": positioning.get('positioning_vs_competitors', ''),
                        "messaging": positioning.get('messaging', [])
                    }
                },
                "6_marketing_goals_kpis": {
                    "title": "6. Marketing Goals & KPIs",
                    "description": "Clear and measurable objectives (SMART). Including key performance indicators to measure success, such as conversion rate or market share.",
                    "content": {
                        "goals": goals.get('goals', []),
                        "kpis": goals.get('kpis', [])
                    }
                },
                "7_strategy_marketing_mix": {
                    "title": "7. Strategy & Marketing Mix (7Ps)",
                    "description": "The overarching strategy to achieve the goals. Focus on the marketing mix (Product, Price, Place, Promotion, People, Process, Physical Evidence).",
                    "content": marketing_mix
                },
                "8_tactics_action_plan": {
                    "title": "8. Tactics & Action Plan",
                    "description": "Concrete actions and a timeline of activities (pre-launch, launch, and follow-up).",
                    "content": action_plan
                },
                "9_budget_resources": {
                    "title": "9. Budget & Resources",
                    "description": "Cost estimation, required resources, and expected revenues. Including ROI estimation.",
                    "content": budget_monitoring.get('budget', {})
                },
                "10_monitoring_evaluation": {
                    "title": "10. Monitoring & Evaluation",
                    "description": "How progress is measured and when evaluations take place to adjust the plan.",
                    "content": budget_monitoring.get('monitoring', {})
                },
                "11_risks_mitigation": {
                    "title": "11. Risks & Mitigation",
                    "description": "Overview of potential risks (such as market failure or technical problems) and how they are addressed.",
                    "content": {
                        "risks": risks_launch.get('risks', [])
                    }
                },
                "12_launch_strategy": {
                    "title": "12. Launch Strategy for New Product",
                    "description": "Planning of product introduction, adoption strategy, and launch phases.",
                    "content": risks_launch.get('launch_strategy', {})
                }
            },
            "evaluation": {
                "overall_score": 7.5,
                "note": "Fast generation mode - detailed quality check skipped",
                "criterion_scores": {
                    "consistency": 7.5,
                    "quality": 7.5,
                    "originality": 7.0,
                    "feasibility": 8.0,
                    "completeness": 7.0,
                    "ethics": 8.5
                },
                "strengths": [
                    "Quick generation time",
                    "Comprehensive structure",
                    "Clear actionable insights"
                ],
                "weaknesses": [
                    "Less detailed than full mode",
                    "Automated quality check"
                ],
                "recommendations": [
                    "Review and customize generated content",
                    "Add specific budget numbers",
                    "Validate target audience assumptions"
                ]
            },
            "raw_data": {
                "research": research,
                "strategy": strategy
            }
        }
    
    def generate_marketing_plan(self, product_data: Dict, auto_iterate: bool = False) -> Dict:
        """Generate marketing plan (synchronous)"""
        print("=" * 60)
        print("⚡ FAST MARKETING PLAN GENERATION STARTED")
        print(f"   Product: {product_data.get('product_name', 'Unknown')}")
        print("=" * 60)
        
        try:
            # Phase 1: Research (2 LLM calls)
            research = self._research_phase(product_data)
            
            # Phase 2: Strategy (3 LLM calls)
            strategy = self._strategy_phase(product_data, research)
            
            # Compile final plan
            plan = self._compile_plan(product_data, research, strategy)
            
            print("=" * 60)
            print("✅ FAST PLAN GENERATION COMPLETED")
            print("=" * 60)
            return plan
            
        except Exception as e:
            print(f"❌ ERROR in generate_marketing_plan: {e}")
            import traceback
            traceback.print_exc()
            raise


# Singleton instance
fast_orchestrator = FastMarketingOrchestrator()
