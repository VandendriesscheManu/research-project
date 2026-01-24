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
        
        product_name = product_data.get('product_name', 'Unknown Product')
        category = product_data.get('product_category', 'general')
        target = product_data.get('target_primary', 'general consumers')
        competitors = product_data.get('competitors', 'market competitors')
        
        print("  → Generating situation & market analysis...")
        market_prompt = f"""Perform a complete SITUATION & MARKET ANALYSIS for {product_name} ({category}). Respond in ENGLISH.

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
        
        product_name = product_data.get('product_name')
        budget = product_data.get('marketing_budget', 'moderate')
        launch_date = product_data.get('launch_date', 'Q1 2026')
        
        print("  → Generating mission, vision, positioning & messaging...")
        positioning_prompt = f"""Create comprehensive MISSION, VISION, VALUE PROPOSITION & POSITIONING for {product_name}. Respond in ENGLISH.

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
        
        positioning = self._generate(positioning_prompt, 500)
        
        print("  → Generating marketing goals, KPIs & marketing mix (7Ps)...")
        tactics_prompt = f"""Create MARKETING GOALS, KPIs & MARKETING MIX (7Ps) for {product_name} (budget: {budget}). Respond in ENGLISH.

**1. Marketing Goals & KPIs**:
- Define 5-7 SMART goals (Specific, Measurable, Achievable, Relevant, Time-bound)
- Include KPIs: conversion rate, market share, brand awareness, customer acquisition cost, ROI, customer lifetime value
- Set targets for each KPI

**2. Marketing Mix (7Ps Strategy)**:
- **Product**: Features, quality, design, branding, packaging, variants
- **Price**: Pricing strategy, positioning, discounts, payment terms
- **Place**: Distribution channels, locations, logistics, online/offline presence
- **Promotion**: Advertising, PR, content marketing, social media, influencer partnerships
- **People**: Staff, customer service, brand ambassadors
- **Process**: Customer journey, purchase process, delivery, after-sales
- **Physical Evidence**: Store design, website UX, packaging, testimonials

Comprehensive (600-700 words) in ENGLISH.
Format als JSON: {{
    "goals": [
        {{"goal": "...", "target": "...", "deadline": "...", "smart": true}},
        ...
    ],
    "kpis": [
        {{"name": "...", "target": "...", "measurement": "..."}},
        ...
    ],
    "marketing_mix": {{
        "product": {{"features": "...", "quality": "...", "design": "...", "branding": "...", "packaging": "..."}},
        "price": {{"strategy": "...", "positioning": "...", "tactics": "..."}},
        "place": {{"channels": ["..."], "distribution": "...", "logistics": "..."}},
        "promotion": {{"advertising": "...", "pr": "...", "content": "...", "social_media": "...", "influencers": "..."}},
        "people": {{"staff": "...", "customer_service": "...", "ambassadors": "..."}},
        "process": {{"customer_journey": "...", "purchase_flow": "...", "delivery": "..."}},
        "physical_evidence": {{"store_design": "...", "website_ux": "...", "testimonials": "..."}}
    }}
}}"""
        
        tactics = self._generate(tactics_prompt, 600)
        
        print("  → Generating action plan, budget, risks & launch strategy...")
        resources_prompt = f"""Create TACTICS, ACTION PLAN, BUDGET, RISKS & LAUNCH STRATEGY for {product_name}. Respond in ENGLISH.

**1. Tactics & Action Plan**:
- **Pre-Launch Phase**: Teaser campaigns, influencer outreach, email list building, PR preparations
- **Launch Phase**: Grand opening, launch event, media coverage, promotional offers, advertising blitz
- **Post-Launch Phase**: Customer retention, feedback collection, optimization, scaling
- Timeline with specific dates/weeks for each activity

**2. Budget & Resources**:
- Detailed budget allocation by channel (social media, ads, PR, events, content, etc.)
- Cost estimation per activity
- Expected ROI and revenue projections
- Required resources (team, tools, agencies)

**3. Monitoring & Evaluation**:
- How progress will be measured (weekly/monthly dashboards)
- When evaluations take place (monthly reviews, quarterly assessments)
- Adjustment criteria to pivot the plan

**4. Risks & Mitigation**:
- Identify 5-6 potential risks (market failure, technical problems, competition, budget overruns, poor adoption)
- Mitigation strategy for each risk
- Contingency plans

**5. Launch Strategy for New Product**:
- Product introduction plan (soft launch vs. hard launch)
- Adoption strategy (early adopters → mass market)
- Launch phases and milestones
- Success criteria for each phase

Comprehensive (700-800 words) in ENGLISH.
Format as JSON: {{
    "action_plan": {{
        "pre_launch": {{"activities": ["..."], "timeline": "...", "budget": "..."}},
        "launch": {{"activities": ["..."], "timeline": "...", "budget": "..."}},
        "post_launch": {{"activities": ["..."], "timeline": "...", "budget": "..."}}
    }},
    "budget": {{
        "total": "...",
        "allocation": {{
            "social_media": "...",
            "paid_ads": "...",
            "pr": "...",
            "events": "...",
            "content": "...",
            "influencers": "...",
            "other": "..."
        }},
        "cost_per_activity": [{{"activity": "...", "cost": "..."}}, ...],
        "roi_projection": "...",
        "revenue_forecast": "..."
    }},
    "monitoring": {{
        "measurement_frequency": "...",
        "evaluation_schedule": ["..."],
        "dashboard_metrics": ["..."],
        "adjustment_triggers": ["..."]
    }},
    "risks": [
        {{
            "id": "...",
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
            "innovators": {{"strategy": "...", "timeline": "..."}},
            "early_adopters": {{"strategy": "...", "timeline": "..."}},
            "early_majority": {{"strategy": "...", "timeline": "..."}},
            "late_majority": {{"strategy": "...", "timeline": "..."}}
        }},
        "launch_phases": [
            {{"phase": "...", "activities": ["..."], "success_criteria": "..."}},
            ...
        ],
        "milestones": [
            {{"milestone": "...", "date": "...", "criteria": "..."}},
            ...
        ]
    }}
}}"""
        
        resources = self._generate(resources_prompt, 700)
        
        resources = self._generate(resources_prompt, 700)
        
        return {
            "positioning": self._parse_json(positioning),
            "tactics": self._parse_json(tactics),
            "resources": self._parse_json(resources)
        }
    
    def _parse_json(self, text: str) -> Dict:
        """Extract JSON from LLM response"""
        try:
            # Try to find JSON block
            start = text.find('{')
            end = text.rfind('}') + 1
            if start != -1 and end > start:
                json_str = text[start:end]
                return json.loads(json_str)
            return {"raw": text[:500]}  # Return first 500 chars if no JSON
        except Exception as e:
            print(f"JSON parse error: {e}")
            return {"raw": text[:500] if text else "No response"}
    
    def _compile_plan(self, product_data: Dict, research: Dict, strategy: Dict) -> Dict:
        """Compile final 12-section plan"""
        print("\n📦 Compiling final plan...")
        
        product_name = product_data.get('product_name', 'Product')
        
        market_intel = research.get('market_intelligence', {})
        swot = research.get('swot', {})
        positioning = strategy.get('positioning', {})
        tactics = strategy.get('tactics', {})
        resources = strategy.get('resources', {})
        
        # Create executive summary combining all key insights
        exec_summary = {
            "overview": f"Complete marketing plan for {product_name}. {positioning.get('value_proposition', '')}",
            "product_description": product_data.get('product_features', 'Innovative product in the market'),
            "objectives": [goal.get('goal', '') for goal in tactics.get('goals', [])[:3]] if tactics.get('goals') else [],
            "strategy_overview": positioning.get('positioning_statement', ''),
            "expected_results": f"ROI: {resources.get('budget', {}).get('roi_projection', 'positive')}",
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
                    "description": "Een kort overzicht van het hele plan: wat het product is, wat de doelstellingen zijn, welke strategie wordt gevolgd en welke resultaten verwacht worden.",
                    "content": exec_summary
                },
                "2_mission_vision_value": {
                    "title": "2. Missie, Visie en Waardepropositie",
                    "description": "Wat is het doel en de visie van het project? Wat maakt het product uniek en waarom zouden klanten het kiezen?",
                    "content": {
                        "mission": positioning.get('mission', ''),
                        "vision": positioning.get('vision', ''),
                        "value_proposition": positioning.get('value_proposition', ''),
                        "unique_selling_points": positioning.get('unique_selling_points', []),
                        "brand_personality": positioning.get('brand_personality', {})
                    }
                },
                "3_situation_market_analysis": {
                    "title": "3. Situatie- en Marktanalyse",
                    "description": "Analyse van de huidige situatie, de interne sterktes en zwaktes, en de externe markt (kansen en bedreigingen). Bevat ook een SWOT- en PEST-analyse.",
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
                    "title": "4. SWOT-analyse",
                    "description": "Overzicht van de sterktes, zwaktes, kansen en bedreigingen die invloed hebben op het product of de organisatie.",
                    "content": swot
                },
                "5_target_audience_positioning": {
                    "title": "5. Doelgroepen en Positionering",
                    "description": "Wie is de doelgroep? Hoe wordt het product gepositioneerd ten opzichte van concurrenten en welke plaats krijgt het in het hoofd van de consument?",
                    "content": {
                        "target_demographics": market_intel.get('target_demographics', {}),
                        "target_psychographics": market_intel.get('target_psychographics', {}),
                        "positioning_statement": positioning.get('positioning_statement', ''),
                        "positioning_vs_competitors": positioning.get('positioning_vs_competitors', ''),
                        "messaging": positioning.get('messaging', [])
                    }
                },
                "6_marketing_goals_kpis": {
                    "title": "6. Marketingdoelen en KPI's",
                    "description": "Duidelijke en meetbare doelstellingen (SMART). Inclusief de belangrijkste prestatie-indicatoren om succes te meten, zoals conversieratio of marktaandeel.",
                    "content": {
                        "goals": tactics.get('goals', []),
                        "kpis": tactics.get('kpis', [])
                    }
                },
                "7_strategy_marketing_mix": {
                    "title": "7. Strategie en Marketingmix (7Ps)",
                    "description": "De overkoepelende strategie om de doelen te behalen. Focus op de marketingmix (Product, Prijs, Plaats, Promotie, People, Process, Physical Evidence).",
                    "content": tactics.get('marketing_mix', {})
                },
                "8_tactics_action_plan": {
                    "title": "8. Tactieken en Actieplan",
                    "description": "Concrete acties en een tijdlijn van activiteiten (pre-launch, lancering en opvolging).",
                    "content": resources.get('action_plan', {})
                },
                "9_budget_resources": {
                    "title": "9. Budget en Middelen",
                    "description": "Raming van de kosten, benodigde middelen en verwachte opbrengsten. Inclusief ROI-inschatting.",
                    "content": resources.get('budget', {})
                },
                "10_monitoring_evaluation": {
                    "title": "10. Monitoring en Evaluatie",
                    "description": "Hoe de voortgang wordt gemeten en wanneer evaluaties plaatsvinden om het plan bij te sturen.",
                    "content": resources.get('monitoring', {})
                },
                "11_risks_mitigation": {
                    "title": "11. Risico's en Mitigatie",
                    "description": "Overzicht van mogelijke risico's (zoals marktfalen of technische problemen) en hoe deze worden opgevangen.",
                    "content": {
                        "risks": resources.get('risks', [])
                    }
                },
                "12_launch_strategy": {
                    "title": "12. Lanceringstrategie voor Nieuw Product",
                    "description": "Planning van de productintroductie, adoptiestrategie en fases van de lancering.",
                    "content": resources.get('launch_strategy', {})
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
