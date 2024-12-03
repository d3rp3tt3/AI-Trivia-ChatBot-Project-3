# AI Trivia Chatbot - UNC Bootcamp Project 3

[add bot screenshot]

cUrioBot is a chatbot for playing a trivia game based on a set list of questions and answers. Using retrieval-augmented-generation (RAG) with a pre-trained LLM, the AI agents interact with the user to assess the answer’s level of correctness, to handle fallback and exception messages, and to generate facts based on a question’s topic.

This app can run locally without any external API calls or other external dependencies. We have also enabled it to run on HuggingFace Spaces.

## Installation

This project depends on these technologies and modules:

* Ollama
* mistral:7b-instruct model from ChatOllama
* Python 3.10 or greater
* LangChain (LLM agent interface)
* Gradio (user interface)
* sqlite3
* Pandas

### Try on HuggingFace Spaces

[HuggingFace Spaces - cUrioBot](https://huggingface.co/spaces/JackKuppuswamy/cUrioBot)

### Try locally

cUrioBot is designed to work entirely locally without using external API requests.

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

    **Python virtual environment**

    ```sh
    python3 -m venv <my-venv>
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Install Ollama:**

    Follow the instructions on the [Ollama website](https://ollama.com) to install Ollama.

5. **Pull the mistral:7b-instruct model:**

    After installing Ollama, pull the `mistral:7b-instruct` model by running:

    ```sh
    ollama pull mistral:7b-instruct
    ```

6. **Run the application:**

    ```sh
    python local_quizchatbot.py
    ```

## Methodology and architecture

### Tools and libraries

* Model: Pretrained embedded LLM model for natural language processing and "humanlike" agent workflows (mistral:7b-instruct)
* HuggingFace transformers
* SQLite database for trivia store
* LangChain for AI agent logic
* Retrieval-Augmented Generation (RAG) for using the questions and answers from our cleaned trivia dataset (via database queries)
* NLP, spaCy, and Sci-kit learn for data cleaning and exploration
* HuggingFace Spaces for hosted app
* Unittest for unit and functional testing and bot accuracy evaluation

### Architecture

cUrioBot is written in Python.

[add architecture diagram]

### Datastore

Data is loaded into two SQLite3 database by using Python scripts that create the prod database if it doesn't exist and populate hem with data from the respective CSVs.

* Prod data: `/infra/prod_sql.py`
* Test data: `infra/test_sql.py`

The prod database is `/app/trivia_qa.db` and the test database is `/app/testing_trivia_qa.db`.

### Workflow

[add workflow diagram]

### Testing

To enable testing, we created a set of mock human answers via the `/data/test/build_mock_data.ipynb` Jupyter Notebook. This notebook includes two key pieces of code:

1. Call an LLM to create mock human answers by adding typos
2. Call an LLM to create mock human answers by giving incorrect answers based on the question

The data is cleaned and then saved as a CSV at `/data/test/mock_data.csv`.

The app also includes unit tests, functional, and model evaluation tests:

* Unit: `/app/unit_tests.py`
* Functional: `app/functional_tests.py`
* Model evaluation: `/app/verify_tests.py`

## Data

### Sourcing

cUrioBot is based on a raw dataset of [200,000 Jeopardy questions in a CSV file](https://www.reddit.com/r/datasets/comments/1uyd0t/200000_jeopardy_questions_in_a_json_file/?rdt=43915).

### Exploration and visualization

We reviewed the data for NA's. We checked the number of unique catergories. The column show number was removed as it did not add value. The show date was converted to Date format so it has availability future functions to be added. Many of the columns had a space in the name. They were renamed with _ to make utilizing them more efficient. We also checked the frequency of categories and answers for general information.

### Cleaning and preparing

We explored using a clasifier to reduce the number of categories. Ultimatly we picked 3 clearly labeled categories, we needed to reduce the size of the dataset and this also allowed for clear labels and a category set that was small enough not to overwhelm the end user. 

The cleaned question set is in a CSV file at `/data/prod/JEOPARDY_CSV_TOP3_Categories.csv`.

## User experience

Users interact with cUrioBot through a chat interface, which we built as a proof-of-concept with Gradio. This app can run completely isolated from the Internet locally or in a hosted service, such as HuggingFace Spaces.
