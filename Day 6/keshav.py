from getpass import getpass
from crewai import Agent, Task, Crew, LLM
from crewai.tools import tool
from youtube_transcript_api import YouTubeTranscriptApi
import re

print("=" * 50)
print("       YOUTUBE AI ASSISTANT")
print("=" * 50)

# Get Gemini API Key
api_key = getpass("Enter your Gemini API Key: ").strip()

# Configure Gemini
llm = LLM(
    model="gemini/gemini-3.5-flash",
    api_key=api_key,
    temperature=0.3
)

# Create YouTube Tool
@tool("YouTube Transcript Tool")
def youtube_transcript(video_url: str) -> str:
    """Get the transcript of a YouTube video using its URL."""

    patterns = [
        r"(?:v=)([a-zA-Z0-9_-]{11})",
        r"youtu\.be/([a-zA-Z0-9_-]{11})",
        r"youtube\.com/shorts/([a-zA-Z0-9_-]{11})",
        r"youtube\.com/embed/([a-zA-Z0-9_-]{11})"
    ]

    video_id = None

    for pattern in patterns:
        match = re.search(pattern, video_url)

        if match:
            video_id = match.group(1)
            break

    if not video_id:
        return "Invalid YouTube URL."

    try:
        transcript = YouTubeTranscriptApi().fetch(video_id)

        text = " ".join(
            snippet.text for snippet in transcript.snippets
        )

        return text[:25000]

    except Exception as e:
        return f"Transcript retrieval failed: {str(e)}"


# Create ONE Agent
youtube_agent = Agent(
    role="YouTube AI Assistant",
    goal="Understand YouTube videos and answer user questions accurately.",
    backstory="You are an intelligent AI assistant who analyzes video content and explains it in simple language.",
    llm=llm,
    tools=[youtube_transcript],
    verbose=True,
    allow_delegation=False
)

# Get User Input
video_url = input("\nEnter YouTube Video URL: ").strip()

question = input("\nAsk your question: ").strip()

# Create Task
youtube_task = Task(
    description="""
    The user has provided a YouTube video URL:

    {video_url}

    User Question:
    {question}

    Instructions:

    1. Use the YouTube Transcript Tool to retrieve the transcript.
    2. Understand the transcript.
    3. Answer the user's question based on the video.
    4. Explain the answer in simple language.
    5. Use headings and bullet points wherever necessary.
    6. Do not invent information.
    """,
    expected_output="A clear and accurate answer based on the YouTube video.",
    agent=youtube_agent
)

# Create Crew
crew = Crew(
    agents=[youtube_agent],
    tasks=[youtube_task],
    verbose=True
)

# Execute Crew
print("\nStarting CrewAI Agent...\n")

result = crew.kickoff(
    inputs={
        "video_url": video_url,
        "question": question
    }
)

# Display Result
print("\n" + "=" * 50)
print("              FINAL ANSWER")
print("=" * 50)

print(result.raw)

print("\nAgent execution completed!")