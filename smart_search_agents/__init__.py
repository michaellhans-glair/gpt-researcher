"""
Smart Search Agents - A simplified LangGraph workflow for conducting deep research.

This package provides a streamlined three-agent architecture for research tasks:
- PreAgent: Query preprocessing and research preparation
- SmartResearcherAgent: Deep research using GPTResearcher
- PostAgent: Report post-processing and finalization
"""

from .main import run_smart_search_task
from .agents import SmartSearchOrchestrator, PreAgent, SmartResearcherAgent, WriterAgent

__version__ = "1.0.0"
__all__ = [
    "run_smart_search_task",
    "SmartSearchOrchestrator",
    "PreAgent",
    "SmartResearcherAgent", 
    "WriterAgent" 
] 