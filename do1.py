from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

search_tool = SerperDevTool()

import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
os.environ["OPENAI_API_KEY"] = os.getenv(
    "OPENAI_API_KEY"
)  # Check OpenAI usage here: https://platform.openai.com/usage
os.environ["SERPER_API_KEY"] = os.getenv(
    "SERPER_API_KEY"
)  # serper.dev API key, check usage here: https://serper.dev/dashboard

from langchain_openai import (
    ChatOpenAI,
)  # See list of OpenAI models here: https://platform.openai.com/docs/models

model_cloud = ChatOpenAI(model="gpt-4o")  # Use GPT-4o
# model_cloud = ChatOpenAI(model = 'gpt-4-turbo') # Use GPT-4-Turbo
# model_cloud = ChatOpenAI(model = 'gpt-4') # Use GPT-4
# model_cloud = ChatOpenAI(model = 'gpt-3.5-turbo') # Use GPT-3.5 Turbo

from langchain_community.llms import (
    Ollama,
)  # See list of local models on Ollama here: https://ollama.com/library

# model_local = Ollama(model = "ollama run llama3:70b-instruct-q2_K") # This is the smallest Llama 3 70b model. Quantization: 2-bit, Size: 26GB. Runs extremely slow. Maybe 0.5 words per second.
# model_local = Ollama(model = "llama3:8b-instruct-fp16") # This is the best possible Llama 3 8b model. Quantization: F16, Size: 16GB. Runs slow, but manageable for non interactive runs. Maybe 4 words per second.
model_local = Ollama(
    model="llama3:instruct"
)  # The default Llama 3 8b model. Quantization: 4-bit, Size: 4.7GB. Runs medium speed. Can do an entire prompt in 10-20s. Can use for interactive runs.
# model_local = Ollama(model = "phi3:3.8b-mini-instruct-4k-fp16") # A bigger version of Google Phi3 LLM. Quantization: F16, Size: 7.6GB. Medium speed.
# model_local = Ollama(model = "phi3:instruct") # A tiny but good Google Phi3 LLM. Quantization: 4-bit, Size: 2.3GB. Fast.

email = "Hi, I'm a Nigerian prince and I need your bank details to transfer $10m"
# email = "Hi, this is John your neighbour - your house is on fire!"

# Creating an email classifier agent with verbose mode
classifier = Agent(
    role="Email Classifier",
    goal="Accurately classify email based on importance. Give every email one of these three ratings: 'important', 'casual', 'spam'.",
    backstory="You are an AI agent whose only job is to classify emails accurately and honestly. \
        Your response is for an 'Email Responder' AI agent who will respond to the email based the importance you assign.",
    verbose=False,  # True configures the internal logger to provide detailed execution logs, aiding in debugging and monitoring. Default is False.
    llm=model_cloud,
    allow_delegation=False,  # Agents can delegate tasks or questions to one another, ensuring that each task is handled by the most suitable agent. Default is True.
)

# Creating an email responder agent with verbose mode
responder = Agent(
    role="Email Responder",
    goal="Based on the importance of the email, write a concise and simple response. \
        If the email is rated 'important', write a formal response. If the email is rated 'casual', write a casual response. \
        If the email is rated 'spam', respond with 'Ignore this email, its spam'. No matter what, be concise.",
    backstory="You are an AI agent whose only job is to write short responses to emails based on their importance. \
        The importance will be provided to you by the 'classifier' agent.",
    verbose=False,  # True configures the internal logger to provide detailed execution logs, aiding in debugging and monitoring. Default is False.
    llm=model_cloud,
    allow_delegation=False,  # Agents can delegate tasks or questions to one another, ensuring that each task is handled by the most suitable agent. Default is True.
)

classify_email = Task(
    description=f"Classify the following email for the 'Email Responser' agent: '{email}'.",
    agent=classifier,
    expected_output="One of these three options: 'important', 'casual', 'spam'.",
)

respond_to_email = Task(
    description=f"Based on the importance provided by the 'Email Classifier' agent, write an response to the email: '{email}'.",
    agent=responder,
    expected_output="A very concise response to the email formatted as markdown.",
    context=[classify_email],
    output_file="email-reply.md",  # Example of output customization
)

crew = Crew(
    agents=[classifier, responder],
    tasks=[classify_email, respond_to_email],
    verbose=2,  # The verbosity level for logging during execution: 1 or 2.
    full_output=False,  # Whether the crew should return the full output with all tasks outputs or just the final output.
    process=Process.sequential,  # The process flow (e.g., sequential, hierarchial) the crew follows. Sequential executes tasks sequentially, ensuring tasks are completed in an orderly progression.
)

result = crew.kickoff()

print(
    f"""
    'Classify Email' task completed!
    Task: {classify_email.output.description}
    Output: {classify_email.output.raw_output}
"""
)

print(
    f"""
    'Respond to Email' task completed!
    Task: {respond_to_email.output.description}
    Output: {respond_to_email.output.raw_output}
"""
)

print(
    f"""
    'Crew completed!
    Final Result Output: {result}
"""
)
