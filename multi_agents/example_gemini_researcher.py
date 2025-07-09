#!/usr/bin/env python3
"""
Example script demonstrating how to use the GeminiResearcherAgent and GeminiEditorAgent
in the multi-agents system.

This script shows how to:
1. Use the GeminiResearcherAgent directly
2. Use the GeminiEditorAgent for research planning
3. Use the GeminiChiefEditorAgent for a complete workflow
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the agents
from multi_agents.agents import GeminiResearcherAgent, GeminiEditorAgent, GeminiChiefEditorAgent

async def example_direct_gemini_research():
    """Example of using GeminiResearcherAgent directly."""
    print("=== Direct Gemini Research Example ===")
    
    # Initialize the Gemini researcher agent
    gemini_researcher = GeminiResearcherAgent()
    
    # Example query
    query = "What are the latest developments in quantum computing?"
    
    try:
        # Conduct research using Gemini
        result = await gemini_researcher.research(
            query=query,
            verbose=True
        )
        
        print(f"\nResearch Result:\n{result}")
        
    except Exception as e:
        print(f"Error during research: {e}")

async def example_gemini_editor():
    """Example of using GeminiEditorAgent for research planning."""
    print("\n=== Gemini Editor Example ===")
    
    # Initialize the Gemini editor agent
    gemini_editor = GeminiEditorAgent()
    
    # Mock research state
    research_state = {
        "initial_research": "Quantum computing has made significant progress in recent years with developments in qubit stability and error correction.",
        "task": {
            "model": "gemini-2.0-flash-exp",
            "include_human_feedback": False,
            "max_sections": 5
        },
        "human_feedback": None
    }
    
    try:
        # Plan research using Gemini editor
        plan = await gemini_editor.plan_research(research_state)
        
        print(f"\nResearch Plan:\n{plan}")
        
    except Exception as e:
        print(f"Error during planning: {e}")

async def example_gemini_workflow():
    """Example of using GeminiChiefEditorAgent for a complete workflow."""
    print("\n=== Complete Gemini Workflow Example ===")
    
    # Define a research task
    task = {
        "query": "What are the environmental impacts of renewable energy technologies?",
        "source": "web",
        "verbose": True,
        "model": "gemini-2.0-flash-exp",
        "follow_guidelines": False,
        "guidelines": "",
        "include_human_feedback": False,
        "max_sections": 5
    }
    
    try:
        # Initialize the Gemini chief editor agent
        gemini_chief = GeminiChiefEditorAgent(task=task)
        
        # Run the complete research workflow
        result = await gemini_chief.run_research_task()
        
        print(f"\nWorkflow Result:\n{result}")
        
    except Exception as e:
        print(f"Error during workflow: {e}")

async def example_subtopic_research():
    """Example of using GeminiResearcherAgent for subtopic research."""
    print("\n=== Subtopic Research Example ===")
    
    # Initialize the Gemini researcher agent
    gemini_researcher = GeminiResearcherAgent()
    
    # Parent query and subtopic
    parent_query = "Artificial Intelligence in Healthcare"
    subtopic = "Machine Learning for Medical Diagnosis"
    
    try:
        # Conduct subtopic research
        result = await gemini_researcher.run_subtopic_research(
            parent_query=parent_query,
            subtopic=subtopic,
            verbose=True
        )
        
        print(f"\nSubtopic Research Result:\n{result}")
        
    except Exception as e:
        print(f"Error during subtopic research: {e}")

async def main():
    """Main function to run all examples."""
    print("Gemini Researcher and Editor Agent Examples")
    print("=" * 60)
    
    # Check if GEMINI_API_KEY is set
    if not os.getenv("GEMINI_API_KEY"):
        print("Warning: GEMINI_API_KEY environment variable is not set.")
        print("Please set it to use the Gemini agent.")
        return
    
    # Run examples
    await example_direct_gemini_research()
    await example_gemini_editor()
    await example_subtopic_research()
    await example_gemini_workflow()

if __name__ == "__main__":
    asyncio.run(main()) 