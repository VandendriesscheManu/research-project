"""
Planner Agent - creates the deterministic multi-agent workflow plan.
"""
from typing import Any, Dict, List


class PlannerAgent:
    """Creates the fixed step plan used by the marketing orchestrator."""

    name = "PlannerAgent"

    def create_step_plan(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Return the six-step plan required for marketing plan generation."""
        product_name = product_data.get("product_name", "Unknown Product")
        steps: List[Dict[str, Any]] = [
            {
                "step": 1,
                "agent": "PlannerAgent",
                "action": "Create the step plan for the full multi-agent workflow.",
                "output_key": "step_plan",
            },
            {
                "step": 2,
                "agent": "ResearchAgent",
                "action": "Perform market research and write findings to shared memory.",
                "output_key": "research",
            },
            {
                "step": 3,
                "agent": "StrategyAgent",
                "action": "Create the first marketing strategy using product data and research.",
                "output_key": "initial_strategy",
            },
            {
                "step": 4,
                "agent": "ReviewerAgent",
                "action": "Evaluate the initial strategy and write feedback.",
                "output_key": "review",
            },
            {
                "step": 5,
                "agent": "StrategyAgent",
                "action": "Revise the strategy using ReviewerAgent feedback.",
                "output_key": "revised_strategy",
            },
            {
                "step": 6,
                "agent": "FinalPlanAgent",
                "action": "Compose the final 12-section marketing plan.",
                "output_key": "final_plan",
            },
        ]

        return {
            "product_name": product_name,
            "workflow": "minimal_multi_agent_marketing_plan",
            "steps": steps,
        }


planner_agent = PlannerAgent()
