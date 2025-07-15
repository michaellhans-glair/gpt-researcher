# Smart Search Agents

A simplified LangGraph workflow for conducting deep research using GPT-Researcher with a streamlined three-agent architecture.

## Overview

This workflow consists of three agents working in sequence:

1. **PreAgent** - Pre-processes the query and prepares research parameters
2. **SmartResearcherAgent** - Conducts deep research using GPTResearcher with `report_type=deep`
3. **PostAgent** - Post-processes the research results and finalizes the report

## Architecture

```
PreAgent → SmartResearcherAgent → PostAgent
```

### Agent Roles

- **PreAgent**: Query validation, enhancement, and research strategy preparation
- **SmartResearcherAgent**: Core research using GPTResearcher with deep report type
- **PostAgent**: Report formatting, quality checks, and final output preparation

## Usage

### Running the Workflow

```bash
# Install dependencies
pip install -r requirements.txt

# Run the workflow
python main.py
```

### Using with LangGraph CLI

```bash
# Install LangGraph CLI
pip install langgraph-cli

# Run the graph
langgraph dev agent.py
```

### Programmatic Usage

```python
from smart_search_agents.main import run_smart_search_task

# Run a research task
report = await run_smart_search_task("What are the latest developments in AI?")
print(report)
```

## Configuration

The workflow is configured through `task.json`:

```json
{
  "query": "Your research query here",
  "max_sections": 3,
  "follow_guidelines": false,
  "model": "gpt-4o",
  "guidelines": [
    "The report MUST be written in APA format",
    "Each sub section MUST include supporting sources using hyperlinks"
  ],
  "verbose": true
}
```

## Environment Variables

- `STRATEGIC_LLM`: Override the model specified in task.json
- `LANGCHAIN_API_KEY`: Enable LangSmith tracing
- `LANGCHAIN_TRACING_V2`: Enable LangSmith tracing v2

## Workflow State

The workflow maintains state through the following structure:

```python
{
    "task": task_config,
    "task_id": uuid,
    "query": "research query",
    "pre_agent_output": pre_processing_results,
    "research_report": deep_research_results,
    "post_agent_output": post_processing_results,
    "final_report": final_output
}
```

## Development

### Adding New Agents

1. Create a new agent class in `agents/`
2. Implement the required interface (process method)
3. Add the agent to the orchestrator workflow
4. Update the state schema as needed

### Extending Functionality

- **PreAgent**: Add query analysis, research planning, or parameter optimization
- **SmartResearcherAgent**: Customize research strategies or add specialized research methods
- **PostAgent**: Add report formatting, quality validation, or export functionality

## Dependencies

- `langgraph`: Workflow orchestration
- `gpt_researcher`: Core research functionality
- `colorama`: Terminal output formatting
- `python-dotenv`: Environment variable management

## License

This project follows the same license as the main GPT-Researcher project. 