# AI Trivia Chatbot - UNC Bootcamp Project 3

**Note:** This project is a work in progress.

We will create a chatbot with which a person can interact to play a simple trivia game. The bot will use an established lightweight LLM model and reference a large dataset of questions via Retrieval-Augmented Generation (RAG). We’ll include agentful workflows programmed via prompt engineering and chaining with LangChain.

## Installation

This project depends on these technologies and modules:

* Ollama
* phi3:3.8b model from ChatOllama
* Python 3.10 or greater
* LangChain (LLM agent interface)
* Gradio (user interface)
* sqlite3
* Pandas

1. **Clone the repository:**

    ```sh
    git clone https://github.com/d3rp3tt3/AI-Trivia-ChatBot-Project-3.git
    cd AI-Trivia-ChatBot-Project-3
    ```

2. **Create a virtual environment (optional but recommended):**

    **Conda**

    ```sh
    conda env create --name <my-env>
    ```

    **Pyenv**

    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Install Ollama:**

    Follow the instructions on the [Ollama website](https://ollama.com) to install Ollama.

5. **Pull the phi3:3.8b model:**

    After installing Ollama, pull the `phi3:3.8b` model by running:

    ```sh
    ollama pull phi3:3.8b
    ```

6. **Run the application:**

    ```sh
    python local_quizchatbot.py
    ```

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
