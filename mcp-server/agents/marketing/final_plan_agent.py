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
        marketing_mix = revised_strategy.get("marketing_mix", {})
        action_plan = revised_strategy.get("action_plan", {})
        budget = revised_strategy.get("budget", {})
        monitoring = revised_strategy.get("monitoring", {})
        risks = revised_strategy.get("risks", {})
        launch_strategy = revised_strategy.get("launch_strategy", {})

        market_analysis = research.get("market_analysis", {})
        target_audience = research.get("target_audience", {})
        competitor_analysis = research.get("competitor_analysis", {})
        swot_analysis = research.get("swot_analysis", {})
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


final_plan_agent = FinalPlanAgent()
