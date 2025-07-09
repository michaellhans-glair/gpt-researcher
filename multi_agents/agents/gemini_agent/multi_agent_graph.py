import os
from typing import TypedDict, Annotated
from dataclasses import dataclass, field

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.types import Send
from langgraph.graph import StateGraph, START, END
from langchain_core.runnables import RunnableConfig
from langchain_google_genai import ChatGoogleGenerativeAI

from gemini_agent.state import OverallState
from gemini_agent.configuration import Configuration
from gemini_agent.graph import graph as pro_search_agent

load_dotenv()

if os.getenv("GEMINI_API_KEY") is None:
    raise ValueError("GEMINI_API_KEY is not set")


# Extended state for multi-agent workflow
class MultiAgentState(TypedDict):
    messages: Annotated[list, "add_messages"]
    pre_processing_result: str
    search_agent_result: str
    post_processing_result: str
    final_response: str


# Pre-processing agent node
def pre_processing_agent(state: MultiAgentState, config: RunnableConfig) -> MultiAgentState:
    """Pre-processing agent that analyzes and prepares the user query before search.
    
    This agent can:
    - Analyze the query complexity
    - Determine if search is needed
    - Prepare optimized search parameters
    - Add context or clarification to the query
    """
    configurable = Configuration.from_runnable_config(config)
    
    # Initialize LLM
    llm = ChatGoogleGenerativeAI(
        model=configurable.query_generator_model,
        temperature=0.7,
        max_retries=2,
        api_key=os.getenv("GEMINI_API_KEY"),
    )
    
    # Get the user's original message
    user_message = ""
    for message in state["messages"]:
        if isinstance(message, HumanMessage):
            user_message = message.content
            break
    
    # Pre-processing prompt
    pre_processing_prompt = f"""
    You are a pre-processing agent that analyzes user queries before they are sent to a search agent.
    
    User Query: {user_message}
    
    Your task is to:
    1. Analyze the query complexity and intent
    2. Determine if this query requires web search
    3. Prepare an optimized version of the query for search
    4. Add any necessary context or clarification
    
    Please provide your analysis and the optimized query for the search agent.
    """
    
    result = llm.invoke(pre_processing_prompt)
    
    return {
        "pre_processing_result": result.content,
        "messages": state["messages"]  # Pass through the original messages
    }


# Post-processing agent node
def post_processing_agent(state: MultiAgentState, config: RunnableConfig) -> MultiAgentState:
    """Post-processing agent that refines and formats the search results.
    
    This agent can:
    - Summarize and organize search results
    - Add additional insights or recommendations
    - Format the response for better readability
    - Cross-reference information from multiple sources
    """
    configurable = Configuration.from_runnable_config(config)
    
    # Initialize LLM
    llm = ChatGoogleGenerativeAI(
        model=configurable.answer_model,
        temperature=0.3,
        max_retries=2,
        api_key=os.getenv("GEMINI_API_KEY"),
    )
    
    # Post-processing prompt
    post_processing_prompt = f"""
    You are a post-processing agent that refines and enhances search results.
    
    Original User Query: {state.get('messages', [])}
    Pre-processing Analysis: {state.get('pre_processing_result', '')}
    Search Agent Results: {state.get('search_agent_result', '')}
    
    Your task is to:
    1. Review and organize the search results
    2. Add additional insights or recommendations
    3. Format the response for better readability
    4. Ensure the response directly addresses the user's original query
    5. Provide a comprehensive and well-structured final answer
    
    Please provide the final refined response.
    """
    
    result = llm.invoke(post_processing_prompt)
    
    return {
        "post_processing_result": result.content,
        "final_response": result.content
    }


# Coordinator function to run the pro-search-agent
def run_search_agent(state: MultiAgentState, config: RunnableConfig) -> MultiAgentState:
    """Coordinates the execution of the pro-search-agent with the current state."""
    
    # Prepare the state for the pro-search-agent
    search_state = {
        "messages": state["messages"],
        "search_query": [],
        "web_research_result": [],
        "sources_gathered": [],
        "initial_search_query_count": 3,
        "max_research_loops": 2,
        "research_loop_count": 0,
        "reasoning_model": "gemini-2.0-flash-exp"
    }
    
    # Run the pro-search-agent
    search_result = pro_search_agent.invoke(search_state, config)
    
    # Extract the final answer from the search agent
    search_agent_response = ""
    if "messages" in search_result and search_result["messages"]:
        for message in search_result["messages"]:
            if isinstance(message, AIMessage):
                search_agent_response = message.content
                break
    
    return {
        "search_agent_result": search_agent_response,
        "messages": state["messages"]  # Keep original messages
    }


# Create the multi-agent workflow
def create_multi_agent_workflow():
    """Creates the multi-agent workflow with pre-processing, search, and post-processing agents."""
    
    # Create the workflow graph
    builder = StateGraph(MultiAgentState, config_schema=Configuration)
    
    # Add nodes
    builder.add_node("pre_processing_agent", pre_processing_agent)
    builder.add_node("search_agent", run_search_agent)
    builder.add_node("post_processing_agent", post_processing_agent)
    
    # Define the workflow flow
    builder.add_edge(START, "pre_processing_agent")
    builder.add_edge("pre_processing_agent", "search_agent")
    builder.add_edge("search_agent", "post_processing_agent")
    builder.add_edge("post_processing_agent", END)
    
    return builder.compile(name="multi-agent-workflow")


# Create the compiled workflow
multi_agent_graph = create_multi_agent_workflow() 