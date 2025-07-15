from typing import Dict, Any, Optional
import re
from .utils.views import print_agent_output
from .utils.llms import call_model


class PreAgent:
    def __init__(self, websocket=None, stream_output=None, tone=None, headers=None):
        self.websocket = websocket
        self.stream_output = stream_output
        self.tone = tone
        self.headers = headers or {}

    def _extract_urls(self, query: str) -> list[str]:
        """Extract URLs from the query text"""
        # URL regex pattern
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(url_pattern, query)
        return urls

    async def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process the initial state and prepare for research"""

        task = state.get("task", {})
        query = task.get("query", "")

        if self.websocket and self.stream_output:
            await self.stream_output(
                "logs", "pre_agent", f"Pre-processing query: {query}", self.websocket
            )
        else:
            print_agent_output(f"Pre-processing query: {query}", agent="PRE_AGENT")

        # Extract URLs from query
        query_domains = self._extract_urls(query)

        # Analyze query to determine the best prompt structure/format
        custom_report_prompt = await self._analyze_query_format(query, task)

        pre_agent_output = {
            "enhanced_query": query,
            "research_strategy": "deep_research",
            "pre_processing_complete": True,
            "custom_report_prompt": custom_report_prompt,
            "query_domains": query_domains
        }

        if self.websocket and self.stream_output:
            await self.stream_output(
                "logs", "pre_agent", "Pre-processing completed", self.websocket
            )
        else:
            print_agent_output("Pre-processing completed", agent="PRE_AGENT")

        # Update state with pre-agent output
        state["pre_agent_output"] = pre_agent_output
        state["custom_report_prompt"] = custom_report_prompt

        return state

    async def _analyze_query_format(self, query: str, task: Dict[str, Any]) -> str:
        """Analyze the query to determine the best prompt structure/format"""

        analysis_prompt = [
            {
                "role": "system",
                "content": """You are an expert at analyzing research queries and classifying them into one of five response formats.

Your task is to read the user's full query and classify it strictly into one of the following formats:

1. **comparison** - The user is explicitly asking to compare multiple options based on criteria. This includes head-to-head evaluations, ranking, or trade-off discussions.

2. **qna** - The user provides a list of questions (explicit or implied), often using numbering, bullets, or clear interrogatives (what, which, how, etc.). If there are 2 or more distinct questions, use this. This includes investment evaluations framed as multiple sub-questions.

3. **step_by_step** - The user is asking for a guide, process, or tutorial. Look for words like "how to", "guide me through", "steps", or process-oriented goals.

4. **itinerary** - The user is asking for a schedule, travel plan, or multi-day arrangement. Look for travel-related keywords like "trip", "plan", "itinerary", "schedule", "days", etc.

5. **default_report** - Use ONLY if the query is general, open-ended, and doesn't contain multiple distinct questions or comparisons. It often looks like: "Research X", "Tell me about Y", or "Give me an overview of Z".

Always choose the **most specific** match. For example, if the query contains a list of questions, always classify it as `qna`, even if the topic is broad.

Respond with **ONLY** one of the following: comparison, qna, step_by_step, itinerary, default_report.""",
            },
            {
                "role": "user",
                "content": f"Query: {query}",
            },
        ]

        try:
            model = task.get("model", "gpt-4o")
            response = await call_model(analysis_prompt, model)

            # Clean the response to get just the format name
            format_name = response.strip().lower() if response else "default_report"

            # Validate the format name
            valid_formats = [
                "comparison",
                "qna",
                "step_by_step",
                "itinerary",
                "default_report",
            ]
            if format_name not in valid_formats:
                format_name = "default_report"

            return format_name

        except Exception as e:
            if self.websocket and self.stream_output:
                await self.stream_output(
                    "logs",
                    "pre_agent",
                    f"Query format analysis failed: {e}",
                    self.websocket,
                )
            else:
                print_agent_output(
                    f"Query format analysis failed: {e}", agent="PRE_AGENT"
                )

            return "default_report"
