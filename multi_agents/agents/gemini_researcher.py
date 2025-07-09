import os
import sys
import asyncio
from colorama import Fore, Style
from .utils.views import print_agent_output

# Import the Gemini agent components
from .gemini_agent.graph import graph as gemini_graph
from .gemini_agent.configuration import Configuration
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI


class GeminiResearcherAgent:
    """
    A research agent that utilizes the Gemini agent from graph.py for conducting research.
    This agent follows the same interface as ResearchAgent but uses Gemini's advanced
    search and reasoning capabilities.
    """
    
    def __init__(self, websocket=None, stream_output=None, tone=None, headers=None):
        self.websocket = websocket
        self.stream_output = stream_output
        self.headers = headers or {}
        self.tone = tone

    async def _run_gemini_graph_async(self, initial_state, config):
        """Run the Gemini graph in a separate thread to avoid blocking."""
        try:
            # Run the Gemini agent in a separate thread to avoid blocking
            result = await asyncio.to_thread(gemini_graph.invoke, initial_state, config)
            return result
        except Exception as e:
            # If the thread approach fails, try with a timeout
            try:
                result = await asyncio.wait_for(
                    asyncio.to_thread(gemini_graph.invoke, initial_state, config),
                    timeout=300  # 5 minute timeout
                )
                return result
            except asyncio.TimeoutError:
                raise Exception("Gemini research timed out after 5 minutes")
            except Exception as inner_e:
                raise Exception(f"Gemini research failed: {str(inner_e)}")

    async def _run_simple_gemini_research(self, query: str):
        """Run simple research using direct Gemini API calls as a fallback."""
        try:
            # Initialize Gemini model
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash-exp",
                temperature=0.7,
                max_retries=2,
                api_key=os.getenv("GEMINI_API_KEY"),
            )
            
            # Create a research prompt
            research_prompt = f"""
            Please conduct comprehensive research on the following topic and provide a detailed analysis:
            
            Topic: {query}
            
            Please provide:
            1. A comprehensive overview of the topic
            2. Key findings and insights
            3. Current trends and developments
            4. Potential implications or future directions
            
            Format your response in a clear, well-structured manner with proper sections and bullet points where appropriate.
            """
            
            # Run the research in a separate thread
            result = await asyncio.to_thread(llm.invoke, research_prompt)
            
            return result.content
            
        except Exception as e:
            raise Exception(f"Simple Gemini research failed: {str(e)}")

    async def research(self, query: str, research_report: str = "research_report",
                       parent_query: str = "", verbose=True, source="web", tone=None, headers=None):
        """Conduct research using the Gemini agent."""
        
        if verbose:
            if self.websocket and self.stream_output:
                await self.stream_output("logs", "gemini_research", f"Starting Gemini research on: {query}", self.websocket)
            else:
                print_agent_output(f"Starting Gemini research on: {query}", agent="GEMINI_RESEARCHER")

        # Prepare the initial state for the Gemini agent
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

        # Configuration for the Gemini agent
        config = {
            "query_generator_model": "gemini-2.0-flash-exp",
            "answer_model": "gemini-2.0-flash-exp",
            "reflection_model": "gemini-2.0-flash-exp",
            "number_of_initial_queries": 3,
            "max_research_loops": 2
        }

        try:
            # Try the full Gemini graph first
            result = await self._run_gemini_graph_async(initial_state, config)
            
            # Extract the final answer from the Gemini agent
            report = ""
            if "messages" in result and result["messages"]:
                for message in result["messages"]:
                    if hasattr(message, 'content'):
                        report = message.content
                        break
            
            if verbose:
                if self.websocket and self.stream_output:
                    await self.stream_output("logs", "gemini_research", f"Gemini research completed for: {query}", self.websocket)
                else:
                    print_agent_output(f"Gemini research completed for: {query}", agent="GEMINI_RESEARCHER")

            return report

        except Exception as e:
            # If the full graph fails, try the simple fallback
            if verbose:
                if self.websocket and self.stream_output:
                    await self.stream_output("logs", "gemini_research", f"Falling back to simple Gemini research for: {query}", self.websocket)
                else:
                    print_agent_output(f"Falling back to simple Gemini research for: {query}", agent="GEMINI_RESEARCHER")
            
            try:
                report = await self._run_simple_gemini_research(query)
                
                if verbose:
                    if self.websocket and self.stream_output:
                        await self.stream_output("logs", "gemini_research", f"Simple Gemini research completed for: {query}", self.websocket)
                    else:
                        print_agent_output(f"Simple Gemini research completed for: {query}", agent="GEMINI_RESEARCHER")
                
                return report
                
            except Exception as fallback_e:
                error_msg = f"Error in Gemini research for query '{query}': {str(e)}. Fallback also failed: {str(fallback_e)}"
                if verbose:
                    if self.websocket and self.stream_output:
                        await self.stream_output("logs", "gemini_research_error", error_msg, self.websocket)
                    else:
                        print_agent_output(error_msg, agent="GEMINI_RESEARCHER")
                raise Exception(error_msg)

    async def run_subtopic_research(self, parent_query: str, subtopic: str, verbose: bool = True, source="web", headers=None):
        """Run research on a subtopic using the Gemini agent."""
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
        """Run initial research using the Gemini agent."""
        task = research_state.get("task")
        query = task.get("query")
        source = task.get("source", "web")

        if self.websocket and self.stream_output:
            await self.stream_output("logs", "initial_research", f"Running initial Gemini research on the following query: {query}", self.websocket)
        else:
            print_agent_output(f"Running initial Gemini research on the following query: {query}", agent="GEMINI_RESEARCHER")
        
        initial_research = await self.research(
            query=query, 
            verbose=task.get("verbose"),
            source=source, 
            tone=self.tone, 
            headers=self.headers
        )
        
        return {"task": task, "initial_research": initial_research}

    async def run_depth_research(self, draft_state: dict):
        """Run in-depth research on a specific topic using the Gemini agent."""
        task = draft_state.get("task")
        topic = draft_state.get("topic")
        parent_query = task.get("query")
        source = task.get("source", "web")
        verbose = task.get("verbose")
        
        if self.websocket and self.stream_output:
            await self.stream_output("logs", "depth_research", f"Running in depth Gemini research on the following report topic: {topic}", self.websocket)
        else:
            print_agent_output(f"Running in depth Gemini research on the following report topic: {topic}", agent="GEMINI_RESEARCHER")
        
        research_draft = await self.run_subtopic_research(
            parent_query=parent_query, 
            subtopic=topic,
            verbose=verbose, 
            source=source, 
            headers=self.headers
        )
        
        return {"draft": research_draft}
