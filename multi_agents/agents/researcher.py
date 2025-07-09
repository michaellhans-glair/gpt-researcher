import os
import sys
from colorama import Fore, Style
from .utils.views import print_agent_output

# Add the agent module to the path to import the pro-search-agent
from .gemini_agent.graph import graph as pro_search_agent
from .gemini_agent.configuration import Configuration
from langchain_core.messages import HumanMessage


class ResearchAgent:
    def __init__(self, websocket=None, stream_output=None, tone=None, headers=None):
        self.websocket = websocket
        self.stream_output = stream_output
        self.headers = headers or {}
        self.tone = tone

    async def research(self, query: str, research_report: str = "research_report",
                       parent_query: str = "", verbose=True, source="web", tone=None, headers=None):
        """Conduct research using the pro-search-agent instead of GPTResearcher."""
        
        if verbose:
            if self.websocket and self.stream_output:
                await self.stream_output("logs", "research", f"Starting research on: {query}", self.websocket)
            else:
                print_agent_output(f"Starting research on: {query}", agent="RESEARCHER")

        # Prepare the state for the pro-search-agent
        initial_state = {
            "messages": [HumanMessage(content=query)],
            "search_query": [],
            "web_research_result": [],
            "sources_gathered": [],
            "initial_search_query_count": 3,
            "max_research_loops": 2,
            "research_loop_count": 0,
            "reasoning_model": "gemini-2.0-flash-exp"
        }

        # Configuration for the pro-search-agent
        config = {
            "query_generator_model": "gemini-2.0-flash-exp",
            "answer_model": "gemini-2.0-flash-exp",
            "reflection_model": "gemini-2.0-flash-exp",
            "number_of_initial_queries": 3,
            "max_research_loops": 2
        }

        try:
            # Run the pro-search-agent
            result = pro_search_agent.invoke(initial_state, config)
            
            # Extract the final answer from the search agent
            report = ""
            if "messages" in result and result["messages"]:
                for message in result["messages"]:
                    if hasattr(message, 'content'):
                        report = message.content
                        break
            
            if verbose:
                if self.websocket and self.stream_output:
                    await self.stream_output("logs", "research", f"Research completed for: {query}", self.websocket)
                else:
                    print_agent_output(f"Research completed for: {query}", agent="RESEARCHER")

            return report

        except Exception as e:
            error_msg = f"Error in research for query '{query}': {str(e)}"
            if verbose:
                if self.websocket and self.stream_output:
                    await self.stream_output("logs", "research_error", error_msg, self.websocket)
                else:
                    print_agent_output(error_msg, agent="RESEARCHER")
            raise Exception(error_msg)

    async def run_subtopic_research(self, parent_query: str, subtopic: str, verbose: bool = True, source="web", headers=None):
        """Run research on a subtopic using the pro-search-agent."""
        try:
            # Combine parent query and subtopic for better context
            combined_query = f"{parent_query} - {subtopic}"
            report = await self.research(
                query=combined_query,
                research_report="subtopic_report", 
                verbose=verbose, 
                source=source, 
                tone=self.tone, 
                headers=headers
            )
        except Exception as e:
            print(f"{Fore.RED}Error in researching topic {subtopic}: {e}{Style.RESET_ALL}")
            report = None
        return {subtopic: report}

    async def run_initial_research(self, research_state: dict):
        """Run initial research using the pro-search-agent."""
        task = research_state.get("task")
        query = task.get("query")
        source = task.get("source", "web")

        if self.websocket and self.stream_output:
            await self.stream_output("logs", "initial_research", f"Running initial research on the following query: {query}", self.websocket)
        else:
            print_agent_output(f"Running initial research on the following query: {query}", agent="RESEARCHER")
        
        initial_research = await self.research(
            query=query, 
            verbose=task.get("verbose"),
            source=source, 
            tone=self.tone, 
            headers=self.headers
        )
        
        return {"task": task, "initial_research": initial_research}

    async def run_depth_research(self, draft_state: dict):
        """Run in-depth research on a specific topic using the pro-search-agent."""
        task = draft_state.get("task")
        topic = draft_state.get("topic")
        parent_query = task.get("query")
        source = task.get("source", "web")
        verbose = task.get("verbose")
        
        if self.websocket and self.stream_output:
            await self.stream_output("logs", "depth_research", f"Running in depth research on the following report topic: {topic}", self.websocket)
        else:
            print_agent_output(f"Running in depth research on the following report topic: {topic}", agent="RESEARCHER")
        
        research_draft = await self.run_subtopic_research(
            parent_query=parent_query, 
            subtopic=topic,
            verbose=verbose, 
            source=source, 
            headers=self.headers
        )
        
        return {"draft": research_draft}