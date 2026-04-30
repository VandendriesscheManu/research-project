"""
Agent Orchestrator - coordinates the minimal marketing multi-agent workflow.
"""
from typing import Any, Dict

from .agent_memory import AgentMemory
from .creative_strategy_agent import creative_strategy_agent
from .evaluator_agent import evaluator_agent
from .final_plan_agent import final_plan_agent
from .market_research_agent import market_research_agent
from .planner_agent import planner_agent


class AgentOrchestrator:
    """Synchronous multi-agent marketing plan orchestrator."""

    def __init__(
        self,
        planner=planner_agent,
        research_agent=market_research_agent,
        strategy_agent=creative_strategy_agent,
        reviewer_agent=evaluator_agent,
        final_agent=final_plan_agent,
    ) -> None:
        self.planner = planner
        self.research_agent = research_agent
        self.strategy_agent = strategy_agent
        self.reviewer_agent = reviewer_agent
        self.final_agent = final_agent

    def generate_marketing_plan(self, product_data: Dict[str, Any], auto_iterate: bool = False) -> Dict[str, Any]:
        """
        Generate a marketing plan through the requested multi-agent sequence.

        auto_iterate is accepted for MCP compatibility. The current workflow
        always performs one reviewer-guided revision.
        """
        memory = AgentMemory()
        product_name = product_data.get("product_name", "Unknown Product")

        print("=" * 60)
        print("MULTI-AGENT MARKETING PLAN GENERATION STARTED")
        print(f"   Product: {product_name}")
        print("=" * 60)

        memory.add_trace("AgentOrchestrator", "Started marketing plan generation", {"product_name": product_name})

        step_plan = self.planner.create_step_plan(product_data)
        memory.write("step_plan", step_plan, self.planner.name)

        memory.add_trace("ResearchAgent", "Started market research")
        research = self.research_agent.conduct_full_research(product_data)
        memory.write("research", research, "ResearchAgent")

        memory.add_trace("StrategyAgent", "Started initial strategy")
        initial_strategy = self.strategy_agent.develop_full_strategy(product_data, research)
        memory.write("initial_strategy", initial_strategy, "StrategyAgent")

        memory.add_trace("ReviewerAgent", "Started initial strategy review")
        review = self.reviewer_agent.evaluate_full_plan(product_data, research, initial_strategy)
        memory.write("review", review, "ReviewerAgent")

        memory.add_trace("StrategyAgent", "Started reviewer-guided strategy revision")
        revised_strategy = self.strategy_agent.revise_strategy(product_data, research, initial_strategy, review)
        memory.write("revised_strategy", revised_strategy, "StrategyAgent")

        memory.add_trace("FinalPlanAgent", "Started final 12-section plan composition")
        final_plan = self.final_agent.compose_final_plan(product_data, research, revised_strategy, review)
        memory.write("final_plan", final_plan, self.final_agent.name)

        quality_score = final_plan.get("metadata", {}).get("quality_score", 0)
        memory.add_trace("AgentOrchestrator", "Completed marketing plan generation", {"quality_score": quality_score})

        result = {
            "final_plan": final_plan,
            "agent_trace": memory.trace,
            "research": research,
            "initial_strategy": initial_strategy,
            "review": review,
            "revised_strategy": revised_strategy,
            "evaluation": review,
            "quality_score": quality_score,
            # Legacy aliases used by the current backend/frontend flow.
            "metadata": final_plan.get("metadata", {}),
            "sections": final_plan.get("sections", {}),
            "raw_data": {
                "step_plan": step_plan,
                "research": research,
                "initial_strategy": initial_strategy,
                "review": review,
                "revised_strategy": revised_strategy,
            },
        }

        print("=" * 60)
        print("MULTI-AGENT MARKETING PLAN GENERATION COMPLETED")
        print("=" * 60)
        return result


agent_orchestrator = AgentOrchestrator()
