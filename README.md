# CrewAI Agents: Test Implementations

This repo contains test implementations of the CrewAI framework for building teams of AI agents.

Each agent can use either a local Large Language Models (LLMs) using Ollama (such as Meta's Llama 3) or a proprietary cloud LLM (such as OpenAI's GPT-4-Turbo).

## Installation Instructions

### Prerequisites
- [Python 3.x and Pip](https://www.python.org/) Python package manager installed
- [Git](https://git-scm.com/) distributed version control system installed
- [Microsoft Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) installed. If not run the installer, and select 'Desktop development with C++'.

### Installation Steps

1. Download and install [Ollama](https://ollama.com/).

2. Visit [Ollama's LLM Library](https://ollama.com/library) and choose which local model(s) you want. To start with I recommend [Google's tiny Phi-3 model](https://ollama.com/library/phi3).

3. Download and run the model via Windows command line. To download and run Google's tiny Phi-3 3.8b model (uses just 2.3 GB of disk space), simply open a Windows Terminal and type:

    `ollama run phi3:instruct`

4. (OPTIONAL) Download and run any other open source models you want to have locally. The best ones I've found for my laptop (16 GB GPU RAM) are:

    `ollama run llama3:8b-instruct-fp16`

    `ollama run llama3:instruct`

    `ollama run phi3:3.8b-mini-instruct-4k-fp16`

5. Clone this repository:

    `git clone https://github.com/colinmccrae/CrewAITest/`

6. Navigate to the project directory:

    `cd CrewAITest`

7. Run the installation script: `install.bat`. If you do this you can move straight to Step 12. If you don't want to run this batch file, you can alternatively manually swtich to a virtual environment and install the dependencies as per Steps 8-11.

8. Create a virtual environment:

    `python -m venv venv`

9. Activate the virtual environment:

    `venv\Scripts\activate`

10. Install dependencies from requirements.txt

    `pip install -r requirements.txt -U`

11. Create a new file called '.env'.

12. Edit the `.env` file to add your API keys. Enter your [OpenAI](https://platform.openai.com/api-keys) and [Serper](https://serper.dev/api-key) API keys into the .env file, as per example text shown below.
Note: This is only required if you plan to use OpenAI's cloud-based models such as GPT-4 and/or Serper's Google Search API.

```
# OpenAI API Key
OPENAI_API_KEY = "your_openai_api_key"

# Serper.dev API Key
SERPER_API_KEY = "your_serper_api_key"
```

13. Execute any of the CrewAI Python scripts. For example: `python crewaih2g.py`

Note: These are set to use GPT-4-Turbo by default, so you will require API access for these files to run and it will cost you money.

Note: If you get the error "Microsoft Visual C++ 14.0 or greater is required" then install Microsoft Visual C++ Build Tools from [here](https://visualstudio.microsoft.com/visual-cpp-build-tools/). Run the installer, and select 'Desktop development with C++'.



## Local LLMs with Ollama

[Ollama](https://ollama.com/) has an extensive [library](https://ollama.com/library) that is constantly updated with the latest open-source LLMs.

A good place to compare LLMs is the LMSYS Chatbot Arena Leaderboard: [LMSYS Chatbot Arena Leaderboard](https://chat.lmsys.org/?leaderboard).

The top 3 LLMs overall (as of 27/04/2024) are:
1. OpenAI's GPT-4 (proprietary licence).
2. Anthropic's Claude 3 Opus (proprietary licence).
3. Google's Gemini 1.5 Pro (proprietary licence).

The top open source LLMs (as of 27/04/2024) are:
1. Meta's Llama-3-70b-Instruct (Open source: Llama 3 Community licence)
2. Cohere's Command R+ 104b (Open source: CC-BY-NC-4.0 licence)
3. Qwen's Qwen1.5-72B-Chat (Open source: Qianwen licence)

The only issue is these open source models require a lot of GPU RAM to run locally (circa 42 GB / 140 GB for a 70b LMM quantized to 4-bit / FP16)

My local laptop has a NVIDIA GeForce RTX 3080 Ti Mobile with 16 GB of GPU RAM. Hence the sweet spot for me is: <=8b FP16 LLM or <=26b 4-bit LLM.

The top open source LLMs for me are (in order of quality):
1. Meta's Llama-3 8b-Instruct-FP16 16 GB (Open source: Llama 3 Community licence)

```ollama run llama3:8b-instruct-fp16```

2. Meta's Llama-3-8b-Instruct 4-bit 4 GB (Open source: Llama 3 Community licence)

```ollama run llama3:instruct```

3. Google's Phi-3 3.8b-mini-instruct-4k-FP16 7.6 GB (Open source: MIT licence)

```ollama run phi3:3.8b-mini-instruct-4k-fp16```

4. Google's Phi-3 3.8b 4-bit 2.3 GB (Open source: MIT licence)

```ollama run phi3:instruct```


## Cloud LLMs on OpenAI

[OpenAI](https://openai.com/) have a suite of best-in-class proprietary LLMs available via an API for a charge. The top models can be found [here](https://platform.openai.com/docs/models/gpt-4-turbo-and-gpt-4).

The latest and greatest model is: 'gpt-4-turbo'.


## Projects in this Repo

Below are the projects I'm currently working on in this repo.

### 1. crewaih2g.py

This is an example that originated in the CrewAI documentation under [How to Guides -> Getting Started](https://docs.crewai.com/how-to/Creating-a-Crew-and-kick-it-off/).

It defines two agents, a researcher and a writer. The researcher can use the [Serper](https://serper.dev/) Google search API to research the given topic, and once complete can delegate to writer agent who writes up the findings in a blog post report in markdown format.

### 2. do1.py

This is an example from [the tutorial by David Ondrej](https://www.youtube.com/watch?v=i-txsBoTJtI) on his YouTube channel.

It defines two agents, one to classify emails, and one to respond to emails based on the classification of the first agent.


## Further CrewAI Examples

There are plenty more CrewAI example implementations to explore at [this Github repo](https://github.com/joaomdmoura/crewAI-examples).
