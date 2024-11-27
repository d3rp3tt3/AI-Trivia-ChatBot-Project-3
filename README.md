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

We reviewed the data for NA's. We checked the number of unique catergories. The column show number was removed as it did not add value. The show date was converted to Date format so it has availability future functions to be added. Many of the columns had a space in the name. They were renamed with _ to make utilizing them more efficient. We also checked the frequency of categories and answers for general information. 

### Cleaning and preparing

We explored using a clasifier to reduce the number of categories. Ultimatly we picked 3 clearly labeled categories, we needed to reduce the size of the dataset and this also allowed for clear labels and a category set that was small enough not to overwhelm the end user. 

## AI Modeling

We will use a base light-weight LLM model, such as Phi 3 from Ollama, and RAG with our trivia dataset.

## User experience

We will create a web frontend allowing users to interact with the chatbot. This can be Gradio or a simple custom React app. In either case, the user should be able to run the application locally.
