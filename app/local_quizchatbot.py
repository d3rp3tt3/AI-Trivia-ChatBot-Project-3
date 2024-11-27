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
            model="phi3:3.8b",
            temperature=0.7
        )

        # Initialize LLM for fallback responses
        self.fallback_llm = ChatOllama(
            model="qwen2.5:3b",
            temperature=1  # Higher temperature for more varied responses
        )

        # Define prompt template for fallback responses
        self.fallback_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are a friendly and succinct 
            assistant for a trivia game chatbot. 
            Generate a helpful and encouraging message when 
            unexpected input occurs. Include the following elements 
            in your response:
            1. Let the user know you don't understand
            2. Write the user a short poem
            3. Tell the user to select a category to play the game
            4. End with an encouraging statement
            Keep the message no longer than 4 sentences.
            """),
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

    def verify_answer(self, user_answer: str, correct_answer: str) -> bool:
        """Use the LLM to verify if the answer is correct"""
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are a trivia gameshow host for a question and answer style trivia game. 
            Compare the user's answer with the correct answer and determine if they are semantically equivalent.
            You will accept answers that include misspellings and grammar problems. Rather than determining
            if the answer exactly matches the answer from the trivia database, you will act
            like a human trivia gameshow host and be flexible on some variance on the answer.
            Respond with only 'True' if correct or 'False' if incorrect."""),
            HumanMessage(content=f"""
            Correct answer: {correct_answer}
            User's answer: {user_answer}
            Are these answers semantically equivalent, even if there are typos or double letters?
            """)
        ])

        response = self.llm.invoke(prompt.format_messages())
        return 'true' in response.content.lower()


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

Would you like to try again? Here are the available categories:

{}
Type a number to select a category, or ask me anything else you'd like to know!""".format(chatbot_instance.get_categories())


def chat(message, history, chatbot_instance):
    """
    Handle chat interactions for the quiz game.
    """
    # Initial greeting - this will show when the interface first loads
    if not history:
        categories = chatbot_instance.get_categories()
        return f"Welcome to the Curio Quiz Game! 🎮\n\nPlease select a category by entering its number:\n\n{categories}"

    try:
        # If there's no current question, treat the input as category selection
        if chatbot_instance.current_question is None:
            try:
                category_num = int(message)
                if 1 <= category_num <= len(chatbot_instance.categories):
                    selected_category = chatbot_instance.categories[category_num - 1]
                    question, answer = chatbot_instance.select_question(
                        selected_category)

                    if question is None:
                        return friendly_fallback_response(chatbot_instance)

                    chatbot_instance.current_question = question
                    chatbot_instance.current_answer = answer

                    return f"Category: {selected_category}\n\nQuestion: {question}"
                else:
                    return friendly_fallback_response(chatbot_instance)
            except ValueError:
                return friendly_fallback_response(chatbot_instance)

        # If there is a current question, treat the input as an answer
        else:
            is_correct = chatbot_instance.verify_answer(
                message, chatbot_instance.current_answer)
            response = (
                f"🎉 Correct! Well done!\n"
                if is_correct
                else f"❌ Incorrect. The correct answer was: {chatbot_instance.current_answer}\n"
            )

            # Reset for next question
            chatbot_instance.current_question = None
            chatbot_instance.current_answer = None

            return f"{response}\n\nWould you like to try another question?\nSelect a category:\n\n{chatbot_instance.get_categories()}"

    except Exception as e:
        return friendly_fallback_response(chatbot_instance)


def create_chatbot_interface():
    chatbot_instance = QuizChatbot("trivia_qa.db")

    iface = gr.ChatInterface(
        fn=lambda message, history: chat(message, history, chatbot_instance),
        title="🎯 Curio Trivia",
        description="Test your knowledge with trivia questions! Select a category and answer questions.",
        examples=[{"text": "Start game"}],
        theme="soft",
        chatbot=gr.Chatbot(
            height=500,
            bubble_full_width=False,
        ),
        # textbox=gr.Textbox(
        #    placeholder="Enter category number or your answer",
        #    container=False,
        #    scale=7
        # ),
    )

    return iface


# Launch the interface
if __name__ == "__main__":
    iface = create_chatbot_interface()
    iface.launch()
