import gradio as gr
import pandas as pd
from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage
import random
import sqlite3


class QuizChatbot:
    def __init__(self, db_path: str):
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)

        # Execute a query to retrieve the data
        query = "SELECT * FROM jeopardy"
        self.df = pd.read_sql_query(query, conn)

        # Close the connection
        conn.close()

        self.categories = self.df['Category'].unique().tolist()

        # Initialize the Ollama model for question answering
        self.llm = ChatOllama(
            model="mistral:7b-instruct",
            # model="qwen2.5:3b",
            temperature=0.5
        )

        # Initialize LLM for fallback responses
        self.fallback_llm = ChatOllama(
            # model="phi3:3.8b",
            model="mistral:7b-instruct",
            temperature=0.7  # Higher temperature for more varied responses
        )

        # Define prompt template for fallback responses
        self.fallback_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are a friendly assistant for a trivia game chatbot. Generate a helpful and encouraging message when unexpected input occurs. Include the following elements in your response:
            1. Let the user know you only do trivia and acknowledge the unexpected input
            2. Ask the user to select from list of available categories to get a trivia question: Science, Literature, and American History.
            4. End with a short encouraging statement"""),
            HumanMessage(content="Unexpected input occurred")
        ])

        # Initialize state variables
        self.current_question = None
        self.current_answer = None

    def get_categories(self) -> str:
        """Return formatted list of categories"""
        return "\n".join([f"{i+1}. {cat}" for i, cat in enumerate(self.categories)])

    def select_question(self, category: str) -> tuple:
        """Select a random question from the specified category"""
        category_questions = self.df[self.df['Category'] == category]
        if len(category_questions) == 0:
            return None, None

        question_row = category_questions.sample(n=1).iloc[0]
        return question_row['Question'], question_row['Answer']

    def verify_answer(self, user_answer: str, correct_answer: str) -> dict:
        """Use the LLM to verify if the answer is correct or close"""
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are a trivia gameshow host for a question and answer style trivia game.
            Compare the user's answer with the correct answer and determine if they are:
            1. Exact match
            2. Close match (semantically similar but not identical, and this can include typos or a partial match)
            3. Not a match

            Capitalization and punctuation should be ignored.

            Return one of the following strings:
            'exact_match'
            'close_match'
            'not_a_match'
            """),
            HumanMessage(content=f"""
            Correct answer: {correct_answer}
            User's answer: {user_answer}
            How do these answers compare?
            """)
        ])

        response = self.llm.invoke(prompt.format_messages())
        comparison_result = response.content.strip().lower()

        return {
            'result': comparison_result,
            'user_answer': user_answer,
            'correct_answer': correct_answer
        }

    def get_additional_info(self, question: str) -> str:
        """Generate additional information about the topic of the question"""
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are an informative assistant for a trivia game. Given a question, generate a short paragraph (about 50-75 words) providing interesting facts or background information related to the topic of the question. Avoid repeating any information directly from the question itself."""),
            HumanMessage(content=f"Question: {question}")
        ])

        response = self.llm.invoke(prompt.format_messages())
        return response.content.strip()


def friendly_fallback_response(chatbot_instance):
    """
    Generate a friendly fallback response using an LLM.
    """
    prompt = chatbot_instance.fallback_prompt.format_messages()

    try:
        response = chatbot_instance.fallback_llm.invoke(prompt)
        return f"{response.content}\n\nAvailable categories:\n{chatbot_instance.get_categories()}"
    except Exception as e:
        # Fallback to static message if LLM fails
        print(f"Error generating fallback response: {str(e)}")
        return """Oops! Looks like something went wrong 😅. Don't worry, I'm here to help!

Would you like to try again? Here are the available categories: Science, Literature, and American History.
Type a number to select a category.""".format(chatbot_instance.get_categories())


def chat(message, history, chatbot_instance):
    """
    Handle chat interactions for the quiz game.
    """
    # Initial greeting - this will show when the interface first loads
    if not history:
        categories = chatbot_instance.get_categories()
        return f"Welcome to the cUrioBot Trivia! 🎮\n\nPlease select a category by entering its number or typing its name:\n\n{categories}"

    try:
        # If there's no current question, treat the input as category selection
        if chatbot_instance.current_question is None:
            # Check if the input is a number
            try:
                category_num = int(message)
                if 1 <= category_num <= len(chatbot_instance.categories):
                    selected_category = chatbot_instance.categories[category_num - 1]
                else:
                    return friendly_fallback_response(chatbot_instance)
            except ValueError:
                # If not a number, treat it as a category name
                selected_category = next((cat for cat in chatbot_instance.categories if cat.lower() == message.lower()), None)
                if selected_category is None:
                    return friendly_fallback_response(chatbot_instance)

            question, answer = chatbot_instance.select_question(selected_category)

            if question is None:
                return friendly_fallback_response(chatbot_instance)

            chatbot_instance.current_question = question
            chatbot_instance.current_answer = answer

            return f"Category: {selected_category}\n\nQuestion: {question}"

        # If there is a current question, treat the input as an answer
        else:
            verification_result = chatbot_instance.verify_answer(
                message, chatbot_instance.current_answer)

            if verification_result['result'] == 'exact_match':
                response = "🎉 Correct! Well done!"
            elif verification_result['result'] == 'close_match':
                response = f"""Close! Your answer '{verification_result['user_answer']}' was very good, but the exact answer was '{
                    verification_result['correct_answer']}'. Great job!"""
            else:
                response = f"""Sorry, that wasn't quite right. The correct answer was: {
                    verification_result['correct_answer']}"""

            additional_info = chatbot_instance.get_additional_info(
                chatbot_instance.current_question)

            # Reset for next question
            chatbot_instance.current_question = None
            chatbot_instance.current_answer = None

            return f"{response}\n\nAdditional info:\n{additional_info}\n\nWould you like to try another question?\nSelect a category:\n\n{chatbot_instance.get_categories()}"

    except Exception as e:
        return friendly_fallback_response(chatbot_instance)



def create_chatbot_interface():
    """Creates a Gradio interface for the quiz chatbot.

    Returns:
        iface: Gradio interface
    """
    chatbot_instance = QuizChatbot("trivia_qa.db")

    iface = gr.ChatInterface(
        fn=lambda message, history: chat(message, history, chatbot_instance),
        title="🎯 cUrioBot Trivia",
        description="Test your knowledge with trivia questions! Select a category and answer questions.",
        examples=[{"text": "Start game"}],
        theme="soft",
        chatbot=gr.Chatbot(
            height=500,
            bubble_full_width=False,
        ),
        textbox=gr.Textbox(
            placeholder="Enter category number or name",
            container=False,
            scale=7
        ),
    )

    return iface


# Launch the interface
if __name__ == "__main__":
    iface = create_chatbot_interface()
    iface.launch(share=True)