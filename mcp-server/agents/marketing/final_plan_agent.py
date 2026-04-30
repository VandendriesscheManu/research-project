"""
Final Plan Agent - composes the frontend-compatible 12-section plan.
"""
from datetime import datetime
from typing import Any, Dict, List


class FinalPlanAgent:
    """Builds the final plan from research, revised strategy, and review data."""

    name = "FinalPlanAgent"

    def compose_final_plan(
        self,
        product_data: Dict[str, Any],
        research: Dict[str, Any],
        revised_strategy: Dict[str, Any],
        review: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Compose the legacy-compatible 12-section marketing plan."""
        product_name = product_data.get("product_name", "Product")
        quality_score = self._quality_score(review)

        executive_summary = revised_strategy.get("executive_summary", {})
        mission_vision_value = revised_strategy.get("mission_vision_value", {})
        positioning = revised_strategy.get("positioning", {})
        messaging = revised_strategy.get("messaging", {})
        goals = revised_strategy.get("marketing_goals", {})
        marketing_mix = self._normalize_marketing_mix(
            revised_strategy.get("marketing_mix", {}),
            product_data,
            research,
        )
        action_plan = revised_strategy.get("action_plan", {})
        budget = revised_strategy.get("budget", {})
        monitoring = revised_strategy.get("monitoring", {})
        risks = revised_strategy.get("risks", {})
        launch_strategy = revised_strategy.get("launch_strategy", {})

        market_analysis = research.get("market_analysis", {})
        target_audience = research.get("target_audience", {})
        competitor_analysis = research.get("competitor_analysis", {})
        swot_analysis = self._normalize_swot(research.get("swot_analysis", {}), product_data, research)
        trends = research.get("trends", {})

        metadata = {
            "product_name": product_name,
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "version": "multi_agent_v1",
            "generation_mode": "multi_agent",
            "quality_score": quality_score,
        }

        sections = {
            "1_executive_summary": {
                "title": "1. Executive Summary",
                "description": "A brief overview of the entire plan: what the product is, what the objectives are, which strategy is followed, and what results are expected.",
                "content": self._executive_summary(product_data, executive_summary, goals, quality_score),
            },
            "2_mission_vision_value": {
                "title": "2. Mission, Vision & Value Proposition",
                "description": "What is the goal and vision of the project? What makes the product unique and why would customers choose it?",
                "content": mission_vision_value,
            },
            "3_situation_market_analysis": {
                "title": "3. Situation & Market Analysis",
                "description": "Analysis of the current situation, internal strengths and weaknesses, and the external market (opportunities and threats). Includes SWOT and PEST analysis.",
                "content": {
                    "market_analysis": market_analysis,
                    "target_audience": target_audience,
                    "competitor_analysis": competitor_analysis,
                    "trends": trends,
                },
            },
            "4_swot_analysis": {
                "title": "4. SWOT Analysis",
                "description": "Overview of strengths, weaknesses, opportunities, and threats that impact the product or organization.",
                "content": swot_analysis,
            },
            "5_target_audience_positioning": {
                "title": "5. Target Audience & Positioning",
                "description": "Who is the target audience? How is the product positioned relative to competitors and what place does it occupy in the consumer's mind?",
                "content": {
                    "target_audience": target_audience,
                    "personas": research.get("personas", []),
                    "positioning": positioning,
                    "messaging": messaging,
                },
            },
            "6_marketing_goals_kpis": {
                "title": "6. Marketing Goals & KPIs",
                "description": "Clear and measurable objectives (SMART). Including key performance indicators to measure success, such as conversion rate or market share.",
                "content": goals,
            },
            "7_strategy_marketing_mix": {
                "title": "7. Strategy & Marketing Mix (7Ps)",
                "description": "The overarching strategy to achieve the goals. Focus on the marketing mix (Product, Price, Place, Promotion, People, Process, Physical Evidence).",
                "content": marketing_mix,
            },
            "8_tactics_action_plan": {
                "title": "8. Tactics & Action Plan",
                "description": "Concrete actions and a timeline of activities (pre-launch, launch, and follow-up).",
                "content": action_plan,
            },
            "9_budget_resources": {
                "title": "9. Budget & Resources",
                "description": "Cost estimation, required resources, and expected revenues. Including ROI estimation.",
                "content": budget,
            },
            "10_monitoring_evaluation": {
                "title": "10. Monitoring & Evaluation",
                "description": "How progress is measured and when evaluations take place to adjust the plan.",
                "content": monitoring,
            },
            "11_risks_mitigation": {
                "title": "11. Risks & Mitigation",
                "description": "Overview of potential risks (such as market failure or technical problems) and how they are addressed.",
                "content": risks,
            },
            "12_launch_strategy": {
                "title": "12. Launch Strategy for New Product",
                "description": "Planning of product introduction, adoption strategy, and launch phases.",
                "content": launch_strategy,
            },
        }

        return {
            "metadata": metadata,
            "sections": sections,
            "evaluation": review,
            "raw_data": {
                "research": research,
                "strategy": revised_strategy,
            },
        }

    def _executive_summary(
        self,
        product_data: Dict[str, Any],
        executive_summary: Dict[str, Any],
        goals: Dict[str, Any],
        quality_score: float,
    ) -> Dict[str, Any]:
        """Normalize executive summary content for the existing frontend."""
        if executive_summary:
            summary = dict(executive_summary)
        else:
            summary = {
                "overview": f"Marketing plan for {product_data.get('product_name', 'Product')}",
                "market_opportunity": "Market opportunity summarized from the research phase.",
                "target": product_data.get("target_primary", "Target audience to be refined"),
                "strategy": "Strategy summarized from the revised agent output.",
                "expected_outcomes": "Expected outcomes to be tracked through the KPI plan.",
            }

        primary_goals = goals.get("primary_goals", []) if isinstance(goals, dict) else []
        summary.setdefault("objectives", self._goal_labels(primary_goals))
        summary.setdefault("quality_score", quality_score)
        return summary

    def _goal_labels(self, goals: List[Any]) -> List[str]:
        labels: List[str] = []
        for goal in goals[:3]:
            if isinstance(goal, dict):
                labels.append(str(goal.get("goal", "")))
            else:
                labels.append(str(goal))
        return [label for label in labels if label]

    def _quality_score(self, review: Dict[str, Any]) -> float:
        score = review.get("overall_score", 0)
        try:
            return float(score)
        except (TypeError, ValueError):
            return 0.0

    def _normalize_swot(
        self,
        swot: Dict[str, Any],
        product_data: Dict[str, Any],
        research: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Ensure SWOT always has useful content in all four quadrants."""
        product_name = product_data.get("product_name", "the product")
        category = product_data.get("product_category", "the category")
        usp = product_data.get("product_usp", "its differentiated value proposition")
        target = product_data.get("target_primary", "the target audience")

        market_analysis = research.get("market_analysis", {}) if isinstance(research, dict) else {}
        market_opportunities = market_analysis.get("opportunities", []) if isinstance(market_analysis, dict) else []
        market_threats = market_analysis.get("threats", []) if isinstance(market_analysis, dict) else []

        defaults = {
            "strengths": [
                {
                    "title": "Differentiated value proposition",
                    "description": f"{product_name} can lead with {usp}, giving {target} a clear reason to choose it.",
                },
                {
                    "title": "Focused product story",
                    "description": f"The {category} positioning can be translated into simple, memorable messaging across launch channels.",
                },
            ],
            "weaknesses": [
                {
                    "title": "Brand awareness needs to be built",
                    "description": f"{product_name} will need repeated proof points, testimonials, and launch visibility to earn trust quickly.",
                },
                {
                    "title": "Early assumptions need validation",
                    "description": "Pricing, channel performance, and audience response should be tested during the first campaign cycles.",
                },
            ],
            "opportunities": [
                {
                    "title": "Audience-specific positioning",
                    "description": f"Messaging can be tailored around the needs and buying triggers of {target}.",
                },
                {
                    "title": "Channel learning loop",
                    "description": "Launch data can identify the strongest acquisition channels and guide budget reallocation.",
                },
            ],
            "threats": [
                {
                    "title": "Competitive response",
                    "description": "Competitors may react with pricing pressure, promotional offers, or stronger visibility.",
                },
                {
                    "title": "Execution complexity",
                    "description": "Weak launch coordination across content, distribution, and customer support can dilute the campaign.",
                },
            ],
        }

        if market_opportunities:
            defaults["opportunities"].append(
                {
                    "title": "Market opportunity",
                    "description": self._stringify(market_opportunities[0]),
                }
            )
        if market_threats:
            defaults["threats"].append(
                {
                    "title": "Market threat",
                    "description": self._stringify(market_threats[0]),
                }
            )

        normalized: Dict[str, Any] = {}
        for key, fallback in defaults.items():
            value = swot.get(key, []) if isinstance(swot, dict) else []
            normalized[key] = self._filled_list(value, fallback)
        return normalized

    def _normalize_marketing_mix(
        self,
        marketing_mix: Dict[str, Any],
        product_data: Dict[str, Any],
        research: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Ensure the marketing mix always covers all seven Ps."""
        product_name = product_data.get("product_name", "the product")
        price = product_data.get("suggested_price", "the planned price point")
        channels = product_data.get("marketing_channels", "the priority launch channels")
        distribution = product_data.get("distribution_channels", "the selected distribution channels")
        target = product_data.get("target_primary", "the target audience")
        usp = product_data.get("product_usp", "the core value proposition")

        aliases = {
            "product": ["product"],
            "price": ["price", "pricing"],
            "place": ["place", "distribution"],
            "promotion": ["promotion", "promotions"],
            "people": ["people"],
            "process": ["process"],
            "physical_evidence": ["physical_evidence", "physical evidence", "physicalEvidence"],
        }

        defaults = {
            "product": {
                "strategy": f"Position {product_name} around {usp}.",
                "details": [
                    "Highlight the most valuable features in launch messaging.",
                    "Connect benefits directly to the customer's problem and desired outcome.",
                    "Keep product claims specific, believable, and easy to compare.",
                ],
            },
            "price": {
                "strategy": f"Use {price} as the reference point and frame value clearly against alternatives.",
                "details": [
                    "Explain what customers receive for the price.",
                    "Use launch offers carefully without weakening long-term perceived value.",
                    "Track conversion rate and margin to validate pricing assumptions.",
                ],
            },
            "place": {
                "strategy": f"Prioritize availability through {self._stringify(distribution)}.",
                "details": [
                    "Make the path to purchase simple and visible from every campaign touchpoint.",
                    "Align distribution promises with actual fulfillment capacity.",
                    "Remove friction from checkout, delivery, and customer support handoffs.",
                ],
            },
            "promotion": {
                "strategy": f"Use {self._stringify(channels)} to reach {target} with consistent launch messaging.",
                "details": [
                    "Build awareness with educational and proof-led content.",
                    "Retarget engaged prospects with stronger conversion messages.",
                    "Coordinate PR, social, email, and paid activity around the launch calendar.",
                ],
            },
            "people": {
                "strategy": "Equip every customer-facing role with the same product story, proof points, and response playbook.",
                "details": [
                    "Prepare support scripts for common questions and objections.",
                    "Identify internal owners for campaign performance, content, and customer feedback.",
                    "Use advocates, creators, or ambassadors where trust is important.",
                ],
            },
            "process": {
                "strategy": "Design a clear journey from first awareness to purchase, onboarding, and retention.",
                "details": [
                    "Map each step of the customer journey and remove unnecessary friction.",
                    "Define follow-up flows for leads, cart abandoners, and first-time buyers.",
                    "Review campaign data weekly and adjust offers, messaging, or channels.",
                ],
            },
            "physical_evidence": {
                "strategy": "Make every visible touchpoint reinforce quality, credibility, and brand consistency.",
                "details": [
                    "Use polished website, packaging, product imagery, and testimonials.",
                    "Show real proof such as reviews, demos, guarantees, or certifications.",
                    "Keep visual language consistent across ads, landing pages, and post-purchase materials.",
                ],
            },
        }

        source = marketing_mix if isinstance(marketing_mix, dict) else {}
        normalized: Dict[str, Any] = {}
        for canonical_key, possible_keys in aliases.items():
            value = self._first_present(source, possible_keys)
            normalized[canonical_key] = self._normalize_mix_item(value, defaults[canonical_key])
        return normalized

    def _first_present(self, data: Dict[str, Any], keys: List[str]) -> Any:
        lowered = {str(key).lower(): value for key, value in data.items()}
        for key in keys:
            if key in data:
                return data[key]
            if key.lower() in lowered:
                return lowered[key.lower()]
        return None

    def _normalize_mix_item(self, value: Any, fallback: Dict[str, Any]) -> Dict[str, Any]:
        if isinstance(value, dict):
            normalized = dict(value)
            if not self._has_content(normalized.get("strategy")):
                normalized["strategy"] = fallback["strategy"]
            normalized["details"] = self._filled_list(normalized.get("details", []), fallback["details"])
            return normalized
        if self._has_content(value):
            return {
                "strategy": self._stringify(value),
                "details": fallback["details"],
            }
        return fallback

    def _filled_list(self, value: Any, fallback: List[Any]) -> List[Any]:
        if isinstance(value, list):
            cleaned = [item for item in value if self._has_content(item)]
            return cleaned if cleaned else fallback
        if self._has_content(value):
            return [value]
        return fallback

    def _has_content(self, value: Any) -> bool:
        if value is None:
            return False
        if isinstance(value, str):
            return value.strip() not in {"", "None", "N/A", "[]", "{}"}
        if isinstance(value, (list, dict)):
            return bool(value)
        return True

    def _stringify(self, value: Any) -> str:
        if isinstance(value, list):
            return ", ".join(self._stringify(item) for item in value if self._has_content(item))
        if isinstance(value, dict):
            return ", ".join(
                f"{str(key).replace('_', ' ').title()}: {self._stringify(item)}"
                for key, item in value.items()
                if self._has_content(item)
            )
        return str(value)


final_plan_agent = FinalPlanAgent()
