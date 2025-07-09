# Multi-Agent Workflow

This document describes the new multi-agent workflow that extends the original `pro-search-agent` with additional agents for enhanced processing.

## Overview

The multi-agent workflow consists of three main components:

1. **Pre-processing Agent** - Analyzes and prepares user queries before search
2. **Pro-Search Agent** - Performs web research (existing functionality)
3. **Post-processing Agent** - Refines and formats search results

## Architecture

```
User Query → Pre-processing Agent → Pro-Search Agent → Post-processing Agent → Final Response
```

### Pre-processing Agent
- Analyzes query complexity and intent
- Determines if web search is needed
- Prepares optimized search parameters
- Adds context or clarification to queries

### Pro-Search Agent (Existing)
- Performs web research using Google Search API
- Generates multiple search queries
- Gathers and cites sources
- Provides comprehensive research results

### Post-processing Agent
- Reviews and organizes search results
- Adds additional insights or recommendations
- Formats response for better readability
- Ensures response addresses the original query

## Usage

### Running the Example

```bash
cd backend/src/agent
python example_multi_agent.py
```

### API Endpoint

The multi-agent workflow is available at the `/multi-agent` endpoint when the server is running.

### Programmatic Usage

```python
from gemini_agent.multi_agent_graph import multi_agent_graph
from langchain_core.messages import HumanMessage

# Prepare initial state
initial_state = {
    "messages": [HumanMessage(content="Your query here")],
    "pre_processing_result": "",
    "search_agent_result": "",
    "post_processing_result": "",
    "final_response": ""
}

# Configuration
config = {
    "query_generator_model": "gemini-2.0-flash-exp",
    "answer_model": "gemini-2.0-flash-exp",
    "reflection_model": "gemini-2.0-flash-exp",
    "number_of_initial_queries": 3,
    "max_research_loops": 2
}

# Run the workflow
result = multi_agent_graph.invoke(initial_state, config)
```

## State Structure

The `MultiAgentState` includes:

- `messages`: Original user messages
- `pre_processing_result`: Analysis from pre-processing agent
- `search_agent_result`: Results from the pro-search agent
- `post_processing_result`: Refined results from post-processing agent
- `final_response`: The final formatted response

## Configuration

The workflow uses the same configuration as the original pro-search agent, with additional parameters for the new agents:

- `query_generator_model`: Model for pre-processing agent
- `answer_model`: Model for post-processing agent
- `reflection_model`: Model for reflection (used in pro-search agent)
- `number_of_initial_queries`: Number of search queries to generate
- `max_research_loops`: Maximum research iterations

## Benefits

1. **Enhanced Query Understanding**: Pre-processing agent can better understand complex queries
2. **Improved Results**: Post-processing agent provides better formatting and insights
3. **Modular Design**: Each agent has a specific responsibility
4. **Extensible**: Easy to add more agents or modify existing ones

## Future Enhancements

Potential improvements for the multi-agent workflow:

1. **Conditional Routing**: Skip certain agents based on query type
2. **Parallel Processing**: Run some agents in parallel
3. **Agent Specialization**: Create specialized agents for different query types
4. **Feedback Loops**: Allow agents to provide feedback to each other
5. **Memory**: Add conversation memory across agents

## Files

- `multi_agent_graph.py`: Main workflow implementation
- `example_multi_agent.py`: Example usage script
- `README_MULTI_AGENT.md`: This documentation file 