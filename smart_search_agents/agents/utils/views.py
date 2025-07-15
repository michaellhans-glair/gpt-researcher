from colorama import Fore, Style
from enum import Enum


class AgentColor(Enum):
    PRE_AGENT = Fore.LIGHTBLUE_EX
    RESEARCHER = Fore.LIGHTGREEN_EX
    POST_AGENT = Fore.LIGHTMAGENTA_EX
    WRITER_AGENT = Fore.LIGHTMAGENTA_EX
    ORCHESTRATOR = Fore.LIGHTYELLOW_EX


def print_agent_output(output: str, agent: str = "RESEARCHER"):
    try:
        color = AgentColor[agent].value
    except KeyError:
        color = Fore.WHITE
    
    print(f"{color}{agent}: {output}{Style.RESET_ALL}") 