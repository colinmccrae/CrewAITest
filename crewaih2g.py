from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
search_tool = SerperDevTool()

import os
from dotenv import load_dotenv
load_dotenv() # Load environment variables from .env file
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY") # Check OpenAI usage here: https://platform.openai.com/usage
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")  # serper.dev API key, check usage here: https://serper.dev/dashboard

from langchain_openai import ChatOpenAI # See list of OpenAI models here: https://platform.openai.com/docs/models/gpt-4-turbo-and-gpt-4
model_cloud = ChatOpenAI(model='gpt-4-turbo') # Use GPT-4-Turbo
# model_cloud = ChatOpenAI(model='gpt-4') # Use GPT-4
# model_cloud = ChatOpenAI(model='gpt-3.5-turbo') # Use GPT-3.5 Turbo

from langchain_community.llms import Ollama # See list of local models on Ollama here: https://ollama.com/library
# model_local = Ollama(model = "ollama run llama3:70b-instruct-q2_K") # This is the smallest Llama 3 70b model. Quantization: 2-bit, Size: 26GB. Runs extremely slow. Maybe 0.5 words per second.
model_local = Ollama(model = "llama3:8b-instruct-fp16") # This is the best possible Llama 3 8b model. Quantization: F16, Size: 16GB. Runs slow, but manageable for non interactive runs. Maybe 4 words per second.
# model_local = Ollama(model = "llama3:instruct") # The default Llama 3 8b model. Quantization: 4-bit, Size: 4.7GB. Runs medium speed. Can do an entire prompt in 10-20s. Can use for interactive runs.
# model_local = Ollama(model = "phi3:3.8b-mini-instruct-4k-fp16") # A bigger version of Google Phi3 LLM. Quantization: F16, Size: 7.6GB. Medium speed.
# model_local = Ollama(model = "phi3:instruct") # A tiny but good Google Phi3 LLM. Quantization: 4-bit, Size: 2.3GB. Fast.

# Creating a senior researcher agent with memory and verbose mode
researcher = Agent(
  role='Senior Researcher',
  goal='Uncover groundbreaking technologies in {topic}',
  verbose=True,
  memory=True,
  backstory=(
    "Driven by curiosity, you're at the forefront of"
    "innovation, eager to explore and share knowledge that could change"
    "the world."
  ),
  tools=[search_tool],
  llm = model_cloud,
  allow_delegation=True
)

# Creating a writer agent with custom tools and delegation capability
writer = Agent(
  role='Writer',
  goal='Narrate compelling tech stories about {topic}',
  verbose=True,
  memory=True,
  backstory=(
    "With a flair for simplifying complex topics, you craft"
    "engaging narratives that captivate and educate, bringing new"
    "discoveries to light in an accessible manner."
  ),
  tools=[search_tool],
  llm = model_cloud,
  allow_delegation=False
)

# Research task
research_task = Task(
  description=(
    "Identify the next big trend in {topic}."
    "Focus on identifying pros and cons and the overall narrative."
    "Your final report should clearly articulate the key points,"
    "its market opportunities, and potential risks."
  ),
  expected_output='A comprehensive 3 paragraphs long report on the latest AI trends.',
  tools=[search_tool],
  agent=researcher,
)

# Writing task with language model configuration
write_task = Task(
  description=(
    "Compose an insightful article on {topic}."
    "Focus on the latest trends and how it's impacting the industry."
    "This article should be easy to understand, engaging, and positive."
  ),
  expected_output='A 4 paragraph article on {topic} advancements formatted as markdown.',
  tools=[search_tool],
  agent=writer,
  async_execution=False,
  output_file='new-blog-post.md'  # Example of output customization
)

# Forming the tech-focused crew with some enhanced configurations
crew = Crew(
  agents=[researcher, writer],
  tasks=[research_task, write_task],
  process=Process.sequential,  # Optional: Sequential task execution is default
  full_output = False, # Whether the crew should return the full output with all tasks outputs or just the final output.
  memory=True, # Utilized for storing execution memories (short-term, long-term, entity memory).
  cache=True, # Specifies whether to use a cache for storing the results of tools' execution.
  max_rpm=100, # Maximum requests per minute the crew adheres to during execution.
)

# Starting the task execution process with enhanced feedback
result = crew.kickoff(inputs={'topic': 'AI in healthcare'})
# print(result)

print(f"""
    'Research Task' task completed!
    Task: {research_task.output.description}
    Output: {research_task.output.raw_output}
""")

print(f"""
    'Write Task' task completed!
    Task: {write_task.output.description}
    Output: {write_task.output.raw_output}
""")

print(f"""
    'Crew completed!
    Final Result Output: {result}
""")