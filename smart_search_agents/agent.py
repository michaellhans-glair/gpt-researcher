from smart_search_agents.agents import SmartSearchOrchestrator

orchestrator = SmartSearchOrchestrator({
  "query": "What are the latest developments in AI research?",
  "max_sections": 3,
  "follow_guidelines": False,
  "model": "gpt-4o",
  "guidelines": [
    "The report MUST be written in APA format",
    "Each sub section MUST include supporting sources using hyperlinks. If none exist, erase the sub section or rewrite it to be a part of the previous section",
    "The report MUST be written in english"
  ],
  "verbose": False
}, websocket=None, stream_output=None)
graph = orchestrator.init_smart_search_team()
graph = graph.compile()
