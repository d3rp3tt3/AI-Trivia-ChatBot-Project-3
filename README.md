# AI Trivia Chatbot - UNC Bootcamp Project 3

**Note:** This project is a work in progress.

We will create a chatbot with which a person can interact to play a simple trivia game. The bot will use an established lightweight LLM model and reference a large dataset of questions via Retrieval-Augmented Generation (RAG). We’ll include agentful workflows programmed via prompt engineering and chaining with LangChain.

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
