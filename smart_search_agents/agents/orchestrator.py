import os
import time
import datetime
from langchain_core.runnables import RunnablePassthrough
from langgraph.graph import StateGraph, END
from typing import Dict, Any, Optional
from gpt_researcher.utils.enum import Tone
from .pre_agent import PreAgent
from .researcher import SmartResearcherAgent
from .writer import WriterAgent
from .utils.views import print_agent_output
from .utils.utils import sanitize_filename
from .memory.research import ResearchState

class SmartSearchOrchestrator:
    def __init__(self, task: Dict[str, Any], websocket=None, stream_output=None, tone=None, headers=None):
        self.task = task
        self.websocket = websocket
        self.stream_output = stream_output
        self.tone = tone
        self.headers = headers or {}
        self.task_id = self._generate_task_id()
        self.output_dir = self._create_output_directory()
        self.config_path = "./agents/config/config.json"

        # Initialize agents
        self.agents = self._initialize_agents()

    def _generate_task_id(self):
        """Generate a unique task ID based on timestamp."""
        return int(time.time())

    def _create_output_directory(self):
        """Create output directory for the research task."""
        output_dir = "./outputs/" + \
            sanitize_filename(
                f"run_{self.task_id}_{self.task.get('query')[0:40]}")
        
        os.makedirs(output_dir, exist_ok=True)
        return output_dir

    def _initialize_agents(self):
        """Initialize all agents for the smart search workflow."""
        return {
            "pre_agent": PreAgent(self.websocket, self.stream_output, self.tone, self.headers),
            "researcher": SmartResearcherAgent(self.websocket, self.stream_output, self.tone, self.headers, self.config_path),
            "writer": WriterAgent(self.websocket, self.stream_output, self.tone, self.headers)
        }

    def _create_workflow(self):
        """Create the workflow graph for smart search."""
        workflow = StateGraph(ResearchState)
        
        # Add nodes for each agent
        workflow.add_node("pre_agent", self.agents["pre_agent"].process)
        workflow.add_node("researcher", self.agents["researcher"].conduct_research)
        workflow.add_node("writer", self.agents["writer"].process)
        
        # Define the workflow edges
        self._add_workflow_edges(workflow)
        
        return workflow

    def _add_workflow_edges(self, workflow):
        """Add edges to the workflow graph."""
        workflow.set_entry_point("pre_agent")
        workflow.add_edge("pre_agent", "researcher")
        workflow.add_edge("researcher", "writer")
        workflow.add_edge("writer", END)

    def init_smart_search_team(self):
        """Initialize the smart search team with the three agents"""
        return self._create_workflow()

    async def _log_research_start(self):
        """Log the start of the research process."""
        message = f"Starting smart search workflow for query '{self.task.get('query')}'..."
        if self.websocket and self.stream_output:
            await self.stream_output("logs", "smart_search_start", message, self.websocket)
        else:
            print_agent_output(message, agent="ORCHESTRATOR")

    async def run_smart_search_task(self, task_id: Optional[str] = None):
        """Run the complete smart search task"""
        
        await self._log_research_start()
        
        # Initialize the graph
        graph = self.init_smart_search_team()
        compiled_graph = graph.compile()
        
        # Run the workflow
        try:
            config = {
                "configurable": {
                    "thread_id": task_id or self.task_id,
                    "thread_ts": datetime.datetime.utcnow()
                }
            }
            
            final_state = await compiled_graph.ainvoke({"task": self.task}, config=config)
            
            if self.websocket and self.stream_output:
                await self.stream_output("logs", "smart_search_complete", "Smart search workflow completed", self.websocket)
            else:
                print_agent_output("Smart search workflow completed", agent="ORCHESTRATOR")
            
            return final_state.get("final_report", final_state.get("research_report", "No report generated"))
            
        except Exception as e:
            error_msg = f"Error in smart search workflow: {str(e)}"
            if self.websocket and self.stream_output:
                await self.stream_output("logs", "error", error_msg, self.websocket)
            else:
                print_agent_output(error_msg, agent="ORCHESTRATOR")
            raise e 