"""
Marketing Agents Module

This module contains the fast marketing plan orchestrator for generating
complete 12-section marketing plans quickly.
"""

from .fast_marketing_orchestrator import fast_orchestrator
from .evaluator_agent import evaluator_agent

__all__ = ['fast_orchestrator', 'evaluator_agent']
