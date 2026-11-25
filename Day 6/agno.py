#agno agent

1. pip install agno 
2. pip install groq
3. pip install ddg(duckduckgo)

import os
from getpass import getpass 
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.websearch import WebSearchTools
from agno.tools.wikipedia import WikipediaTools
os.environ["GROQ_API_KEY"]=getpass("enter groq key")

agent=Agent(
    name="First Agent",
    model=Groq(id="openai/gpt-oss-120b"),
    tools=[WebSearchTools(), WikipediaTools()],
    instructions=[
        "Search the internet for the user's questions",
        "Summarize the information simply",
        "Include source links in your answer"
    ],
    add_history_to_context=True,
    num_history_runs=3,
    markdown=True
)

agent.print_response("Find the latest research paper on AI", stream=True)
agent.print_response("Explain AI using wikipedia", stream=True)