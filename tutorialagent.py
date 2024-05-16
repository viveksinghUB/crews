import os
os.environ["SERPER_API_KEY"] = ""  # serper.dev API key
os.environ["OPENAI_API_KEY"] = ""



from crewai import Agent
from crewai_tools import SerperDevTool
from crewai import Task
from crewai import Crew, Process

search_tool = SerperDevTool()

# Creating a senior researcher agent with memory and verbose mode
researcher = Agent(
  role='User finding details about companies',
  goal='Find details about {topic}',
  verbose=True,
  memory=True,
  backstory=(
    "Curious to present details about a company in simple form"
    "and explain it."
  ),
  tools=[search_tool],
  allow_delegation=True
)


research_task = Task(
  description=(
    "Find the directors and what the company {topic} works on"
    "Write about how to contact them."
  ),
  expected_output='A small article on {topic} what it does and how to contact it',
  tools=[search_tool],
  agent=researcher,
  async_execution=False,
  output_file='new-blog-post.md'  # Example of output customization
)


# Forming the tech-focused crew with some enhanced configurations
crew = Crew(
  agents=[researcher],
  tasks=[research_task],
  process=Process.sequential,  # Optional: Sequential task execution is default
  memory=True,
  cache=True,
  max_rpm=100,
  share_crew=True
)

# Starting the task execution process with enhanced feedback
result = crew.kickoff(inputs={'topic': 'texmeco'})
print(result)