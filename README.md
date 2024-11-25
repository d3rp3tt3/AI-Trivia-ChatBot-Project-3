# AI Trivia Chatbot - UNC Bootcamp Project 3

**Note:** This project is a work in progress.

We will create a chatbot with which a person can interact to play a simple trivia game. The bot will use an established lightweight LLM model and reference a large dataset of questions via Retrieval-Augmented Generation (RAG). We’ll include agentful workflows programmed via prompt engineering and chaining with LangChain.

## Try the AI QuizBot

**(Coming soon) No installation/config: HuggingFace Spaces**
The simplest way to test the project is to visit the working proof-of-concept on HuggingFace Spaces (coming soon).

**(Works today) Run locally** 
To run the project locally, you will need to install its dependencies and follow the instructions below.

**Note**: We recommend you use a virtual environment to test this project, such as Anaconda environments or Pyenv. You will install the Python dependencies in this virtual environment, which will keep your main/base installs separate and prevent accidental overrides of module versions for your other projects.

### Install dependencies

This project depends on these technologies and modules:

* Ollama
* phi3:3.8b model from ChatOllama
* Python 3.10 or greater
* LangChain (LLM agent interface)
* Gradio (user interface)
* sqlite3
* Pandas

**Note**: If you receive an error that one of the Python modules isn't available, run a `pip install <moduleName>` to install it. For instance, `pip install gradio`.

**Ollama**
[Download and install Ollama](https://ollama.com/download)

Ollama lets you easily download AI models. You pull the model once; therefore, your code isn't manually pulling the model each time it runs.

**Pull the LLM AI model**
After you've installed Ollama, you'll need to get the AI model.

1. In a terminal, run `ollama serve` to start the Ollama server. Keep this terminal open while you are testing the app.
2. In a new terminal,  `ollama pull phi3:3.8b` and wait for the model to be downloaded and installed.

### Run the project

1. Clone this repository's source code.
2. In a terminal, navigate to the the `app` folder in the repository, and run `python quizchatbot.py`
3. Click the URL in the terminal output. This opens a new tab in your browser and show's the app's UI.
4. Play a game with the bot!

## Methodology

### Tools and libraries

* Model: lightweight LLM model, such as Phi 3 on Ollama.
* LangChain for AI agents and chaining
* RAG for using the questions and answers from our cleaned trivia dataset
* NLP - spaCy
* Scikt-learn - TF-IDF, Kmeans, etc.

## Data

### Sourcing

We will use at least one dataset for RAG. [200,000 Jeopardy questions in a JSON file](https://www.reddit.com/r/datasets/comments/1uyd0t/200000_jeopardy_questions_in_a_json_file/?rdt=43915). Stretch: Include one or more additional datasets.

### Exploration and visualization

To better understand the data, we will explore it to determine its data types and existing features.

### Cleaning and preparing

We want to have a small number of top-level categories. However, from our cursory review, trivia datasets often have vague and unique categories. We will likely need to use some NLP tools and TF-IDF with clustering to identify the ideal number of categories and then manually name them.

## AI Modeling

We will use a base light-weight LLM model, such as Phi 3 from Ollama, and RAG with our trivia dataset.

## User experience

We will create a web frontend allowing users to interact with the chatbot. This can be Gradio or a simple custom React app. In either case, the user should be able to run the application locally.
