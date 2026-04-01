from typing import TypedDict, List, Annotated
import operator


class ResearchState(TypedDict):
    task: dict
    research_report: str
    pre_agent_output: dict
    writer_agent_output: dict
    final_report: str





