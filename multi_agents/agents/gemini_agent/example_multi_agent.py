#!/usr/bin/env python3
"""
Example script demonstrating the multi-agent workflow.

This script shows how to use the multi-agent workflow that includes:
1. Pre-processing agent (analyzes and prepares queries)
2. Pro-search-agent (performs web research)
3. Post-processing agent (refines and formats results)
"""

import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

from gemini_agent.multi_agent_graph import multi_agent_graph
from gemini_agent.configuration import Configuration

load_dotenv()

def run_multi_agent_example():
    """Run an example of the multi-agent workflow."""
    
    # Example user query
    user_query = "What are the latest developments in quantum computing?"
    
    # Prepare the initial state
    initial_state = {
        "messages": [HumanMessage(content=user_query)],
        "pre_processing_result": "",
        "search_agent_result": "",
        "post_processing_result": "",
        "final_response": ""
    }
    
    # Configuration for the workflow
    config = {
        "query_generator_model": "gemini-2.0-flash-exp",
        "answer_model": "gemini-2.0-flash-exp",
        "reflection_model": "gemini-2.0-flash-exp",
        "number_of_initial_queries": 3,
        "max_research_loops": 2
    }
    
    print("🤖 Starting Multi-Agent Workflow")
    print("=" * 50)
    print(f"User Query: {user_query}")
    print()
    
    try:
        # Run the multi-agent workflow
        result = multi_agent_graph.invoke(initial_state, config)
        
        print("📋 Workflow Results:")
        print("=" * 50)
        
        print("\n🔍 Pre-processing Agent Analysis:")
        print("-" * 30)
        print(result.get("pre_processing_result", "No pre-processing result"))
        
        print("\n🔎 Search Agent Results:")
        print("-" * 30)
        print(result.get("search_agent_result", "No search results"))
        
        print("\n✨ Post-processing Agent Final Response:")
        print("-" * 30)
        print(result.get("final_response", "No final response"))
        
        print("\n✅ Workflow completed successfully!")
        
    except Exception as e:
        print(f"❌ Error running multi-agent workflow: {e}")
        raise

if __name__ == "__main__":
    # Check if GEMINI_API_KEY is set
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ Error: GEMINI_API_KEY environment variable is not set")
        print("Please set your Gemini API key before running this example.")
        exit(1)
    
    run_multi_agent_example() 