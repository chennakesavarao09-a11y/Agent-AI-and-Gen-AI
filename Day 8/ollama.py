# OLLAMA - Example 1 - Python Interview Agent

from agno.agent import Agent 
from agno.models.ollama import Ollama

model=Ollama(id="llama3.2:1b")

agent=Agent(
    name="pythoninterviewagent",
    model=model,
    instructions="""
    You are a Personal Python Interview Agent
    Rules:
    1. help me to prepare for interview.
    2. Whenever you see python questions then only respond otherwise please say:
    It's not a interview question."""
)
while True:
    user_input=input("\n you").strip()
    if user_input.lower()=="exit":
        print("Bye!")
        break
    response=agent.run(user_input)
    print(response.content)