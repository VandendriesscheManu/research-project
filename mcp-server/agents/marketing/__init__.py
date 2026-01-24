"""
Marketing Agents Module

This module contains specialized agents for creating comprehensive marketing plans:
- Market Research Agent: Analyzes market, competitors, and target audience
- Creative Strategy Agent: Develops marketing strategy and campaigns
- Evaluator Agent: Assesses quality and provides feedback
- Marketing Plan Orchestrator: Coordinates all agents to generate complete plans
"""

from .market_research_agent import MarketResearchAgent
from .creative_strategy_agent import CreativeStrategyAgent
from .evaluator_agent import EvaluatorAgent
from .marketing_plan_orchestrator import MarketingPlanOrchestrator

__all__ = [
    'MarketResearchAgent',
    'CreativeStrategyAgent',
    'EvaluatorAgent',
    'MarketingPlanOrchestrator'
]
