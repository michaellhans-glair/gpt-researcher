# Gemini Researcher and Editor Agents

This document explains how to use the new `GeminiResearcherAgent` and `GeminiEditorAgent` that integrate the Gemini agent from `graph.py` into the multi-agents system.

## Overview

The `GeminiResearcherAgent` and `GeminiEditorAgent` are research agents that utilize Google's Gemini 2.0 Flash model for conducting advanced web research. They follow the same interface as the existing `ResearchAgent` and `EditorAgent` but leverage Gemini's enhanced search and reasoning capabilities.

## Features

- **Advanced Search**: Uses Gemini's native Google Search API integration
- **Multi-loop Research**: Conducts iterative research with reflection and follow-up queries
- **Source Validation**: Automatically validates and cites sources
- **Compatible Interface**: Follows the same interface as other agents in the system
- **WebSocket Support**: Supports real-time streaming of research progress
- **Error Handling**: Robust error handling with detailed logging
- **Research Planning**: Advanced research planning with Gemini's reasoning capabilities
- **Async Support**: Full async/await support to prevent blocking calls

## Prerequisites

1. **GEMINI_API_KEY**: Set your Google Gemini API key as an environment variable
   ```bash
   export GEMINI_API_KEY="your_gemini_api_key_here"
   ```

2. **Dependencies**: Ensure all required packages are installed
   ```bash
   pip install -r multi_agents/requirements.txt
   ```

## Async Implementation

The Gemini agents are designed to work properly in async environments and handle blocking calls gracefully:

### Blocking Call Solutions

The agents use several strategies to handle blocking calls:

1. **Thread-based Execution**: All Gemini API calls are executed in separate threads using `asyncio.to_thread()`
2. **Timeout Protection**: Research operations have a 5-minute timeout to prevent hanging
3. **Fallback Mechanism**: If the complex Gemini graph fails, the agent falls back to simple direct API calls
4. **Error Recovery**: Comprehensive error handling with graceful degradation

### Async Methods

All research methods are properly async:

```python
# All methods are async and won't block the event loop
result = await agent.research("Your query")
result = await agent.run_subtopic_research("Parent", "Subtopic")
result = await agent.run_initial_research(research_state)
result = await agent.run_depth_research(draft_state)
```

## Usage

### 1. Direct Research Usage

```python
from multi_agents.agents import GeminiResearcherAgent

# Initialize the agent
gemini_researcher = GeminiResearcherAgent()

# Conduct research (async)
result = await gemini_researcher.research(
    query="What are the latest developments in quantum computing?",
    verbose=True
)

print(result)
```

### 2. Research Planning with Gemini Editor

```python
from multi_agents.agents import GeminiEditorAgent

# Initialize the Gemini editor agent
gemini_editor = GeminiEditorAgent()

# Mock research state
research_state = {
    "initial_research": "Quantum computing has made significant progress...",
    "task": {
        "model": "gemini-2.0-flash-exp",
        "include_human_feedback": False,
        "max_sections": 5
    },
    "human_feedback": None
}

# Plan research using Gemini editor (async)
plan = await gemini_editor.plan_research(research_state)
print(plan)
```

### 3. Subtopic Research

```python
# Research a specific subtopic (async)
result = await gemini_researcher.run_subtopic_research(
    parent_query="Artificial Intelligence in Healthcare",
    subtopic="Machine Learning for Medical Diagnosis",
    verbose=True
)
```

### 4. Complete Workflow

```python
from multi_agents.agents import GeminiChiefEditorAgent

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

# Initialize the chief editor agent
gemini_chief = GeminiChiefEditorAgent(task=task)

# Run the complete workflow (async)
result = await gemini_chief.run_research_task()
```

### 5. With WebSocket Streaming

```python
async def stream_output(message_type, agent, message, websocket):
    await websocket.send_json({
        "type": message_type,
        "agent": agent,
        "message": message
    })

# Initialize with WebSocket support
gemini_researcher = GeminiResearcherAgent(
    websocket=websocket,
    stream_output=stream_output
)

# Research with real-time updates (async)
result = await gemini_researcher.research(
    query="Your research query here",
    verbose=True
)
```

## Configuration

The Gemini agents use the following default configuration:

```python
config = {
    "query_generator_model": "gemini-2.0-flash-exp",
    "answer_model": "gemini-2.0-flash-exp", 
    "reflection_model": "gemini-2.0-flash-exp",
    "number_of_initial_queries": 3,
    "max_research_loops": 2
}
```

You can customize these settings by modifying the configuration in the agent initialization.

## Agent Interfaces

### GeminiResearcherAgent

The `GeminiResearcherAgent` implements the same interface as `ResearchAgent`:

#### Methods

- `research(query, ...)`: Conduct research on a given query (async)
- `run_subtopic_research(parent_query, subtopic, ...)`: Research a specific subtopic (async)
- `run_initial_research(research_state)`: Run initial research for a task (async)
- `run_depth_research(draft_state)`: Run in-depth research on a topic (async)

### GeminiEditorAgent

The `GeminiEditorAgent` implements the same interface as `EditorAgent`:

#### Methods

- `plan_research(research_state)`: Plan research outline based on initial research (async)
- `run_parallel_research(research_state)`: Execute parallel research tasks for each section (async)

### Parameters

- `websocket`: WebSocket connection for real-time updates
- `stream_output`: Function for streaming output
- `tone`: Research tone/style
- `headers`: Additional headers for API requests

## Integration with Multi-Agents System

The Gemini agents are fully integrated into the multi-agents system and can be used as drop-in replacements for the regular agents:

```python
# In orchestrator.py, replace:
# "research": ResearchAgent(...)
# "editor": EditorAgent(...)
# With:
"research": GeminiResearcherAgent(...)
"editor": GeminiEditorAgent(...)
```

## Example Script

Run the example script to see the Gemini agents in action:

```bash
python multi_agents/example_gemini_researcher.py
```

This script demonstrates:
- Direct research usage
- Research planning with Gemini editor
- Subtopic research
- Complete workflow integration

## Testing

Run the async tests to verify the blocking call fixes:

```bash
python multi_agents/test_async_gemini.py
```

This will test:
- Async method initialization
- Non-blocking method calls
- Error handling in async context

## Error Handling

The agents include comprehensive error handling:

- API key validation
- Network timeout handling
- Search API rate limiting
- Invalid input management
- Source validation errors
- Blocking call prevention
- Fallback mechanism for failed operations

## Performance Considerations

- **Parallel Processing**: The agents can run multiple search queries in parallel
- **Caching**: Results are cached to avoid redundant searches
- **Token Management**: Efficient token usage with source URL resolution
- **Memory Management**: Optimized memory usage for large research tasks
- **Non-blocking**: All operations are async to prevent event loop blocking

## Troubleshooting

### Common Issues

1. **GEMINI_API_KEY not set**
   ```
   Error: GEMINI_API_KEY is not set
   ```
   Solution: Set the environment variable with your Gemini API key

2. **Blocking call errors**
   ```
   Error: Blocking call to socket.socket.connect
   ```
   Solution: The agents now handle this automatically with thread-based execution

3. **Search API errors**
   ```
   Error in Gemini research: Search API rate limit exceeded
   ```
   Solution: Wait and retry, or check your API quota

4. **Model not found**
   ```
   Error: Model gemini-2.0-flash-exp not available
   ```
   Solution: Check if the model name is correct and available in your region

5. **Timeout errors**
   ```
   Error: Gemini research timed out after 5 minutes
   ```
   Solution: The agent will automatically fall back to simple research mode

### Debug Mode

Enable verbose logging to debug issues:

```python
result = await gemini_researcher.research(
    query="Your query",
    verbose=True  # Enable detailed logging
)
```

### Fallback Mechanism

If the complex Gemini graph fails, the agent automatically falls back to simple research:

```python
# The agent will try the full graph first, then fall back to simple research
result = await gemini_researcher.research("Your query")
```

## Contributing

To extend the Gemini agents:

1. Follow the existing code patterns
2. Maintain compatibility with the multi-agents interface
3. Add comprehensive error handling
4. Include unit tests for new functionality
5. Update documentation
6. Ensure all new methods are async

## License

These agents are part of the GPT-Researcher project and follow the same license terms. 