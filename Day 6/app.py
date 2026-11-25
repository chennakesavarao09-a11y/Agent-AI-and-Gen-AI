from agno.agent import Agent
from agno.team import Team
from agno.team.mode import TeamMode
from agno.models.groq import Groq
import os
from getpass import getpass
print("       AGNO MULTI-AGENT SYSTEM")
api_key = getpass("\nEnter your Groq API Key: ")

if not api_key.strip():
    print("API Key cannot be empty!")
    exit()

# Set API key dynamically
os.environ["GROQ_API_KEY"] = api_key.strip()

print("\nAPI Key received successfully!")

model = Groq(id="openai/gpt-oss-120b")

java_agent = Agent(
    name="Java Agent",
    role="Java Programming Specialist",
    model=model,
    instructions=[
        "You are an expert Java programmer.",
        "Answer Java-related questions.",
        "Explain concepts in simple language.",
        "Provide Java code examples when required."
    ],
    markdown=True
)

python_agent = Agent(
    name="Python Agent",
    role="Python Programming Specialist",
    model=model,
    instructions=[
        "You are an expert Python programmer.",
        "Answer Python-related questions.",
        "Explain concepts in simple language.",
        "Provide Python code examples when required."
    ],
    markdown=True
)

sql_agent = Agent(
    name="SQL Agent",
    role="SQL and Database Specialist",
    model=model,
    instructions=[
        "You are an expert SQL programmer.",
        "Answer SQL and database-related questions.",
        "Explain queries step by step.",
        "Provide SQL examples when required."
    ],
    markdown=True
)

team = Team(
    name="Programming Assistant Team",
    members=[
        java_agent,
        python_agent,
        sql_agent
    ],
    model=model,
    mode=TeamMode.route,
    instructions=[
        "You are the Team Leader.",
        "Understand the user's question.",
        "Identify the appropriate specialist.",
        "Java questions must go to Java Agent.",
        "Python questions must go to Python Agent.",
        "SQL questions must go to SQL Agent.",
        "Do not answer specialist questions yourself.",
        "For unrelated questions, explain that you support Java, Python and SQL."
    ],
    markdown=True,
    show_members_responses=True
)
print("       MULTI-AGENT READY")

while True:

    question = input("\nEnter your question (type exit to stop): ")

    if question.lower().strip() == "exit":
        print("\nThank you for using Agno Multi-Agent System!")
        break

    if not question.strip():
        print("Please enter a valid question.")
        continue

    print("\nTeam Leader is assigning your question...\n")

    try:
        team.print_response(
            input=question,
            stream=True
        )

    except Exception as e:
        print("\nError:", e)
        print("Please check your API key, model availability or internet connection.")