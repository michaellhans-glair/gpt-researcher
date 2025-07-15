from gpt_researcher import GPTResearcher
from colorama import Fore, Style
from typing import Dict, Any, Optional
from .utils.views import print_agent_output


class SmartResearcherAgent:
    def __init__(self, websocket=None, stream_output=None, tone=None, headers=None, config_path=None):
        self.websocket = websocket
        self.stream_output = stream_output
        self.headers = headers or {}
        self.tone = tone
        self.config_path = config_path

    async def conduct_research(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Conduct deep research on the given query"""
        
        query = state.get("task", {}).get("query", "")
        task = state.get("task", {})
        pre_agent_output = state.get("pre_agent_output", {})
        query_domains = pre_agent_output.get("query_domains", [])
        
        if self.websocket and self.stream_output:
            await self.stream_output("logs", "researcher", f"Starting deep research on: {query}", self.websocket)
        else:
            print_agent_output(f"Starting deep research on: {query}", agent="RESEARCHER")
        
        try:
            # Initialize the researcher with deep report type
            researcher = GPTResearcher(
                query=query, 
                report_type="deep",  # Using deep research as requested
                parent_query=query,
                verbose=task.get("verbose", True), 
                report_source="web",
                query_domains=query_domains,
                tone=self.tone, 
                websocket=self.websocket, 
                headers=self.headers,
                config_path=self.config_path
            )
            
            # Conduct research
            await researcher.conduct_research()
            
            # Write the report
            research_report = await researcher.write_report()
            
            if self.websocket and self.stream_output:
                await self.stream_output("logs", "researcher", "Deep research completed", self.websocket)
            else:
                print_agent_output("Deep research completed", agent="RESEARCHER")
            
            # Update state with research results
            state["research_report"] = research_report
            
            return state
            
        except Exception as e:
            error_msg = f"Error in deep research: {str(e)}"
            if self.websocket and self.stream_output:
                await self.stream_output("logs", "error", error_msg, self.websocket)
            else:
                print_agent_output(f"{Fore.RED}Error in deep research: {e}{Style.RESET_ALL}", agent="RESEARCHER")
            raise e
