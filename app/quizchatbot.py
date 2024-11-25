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

        # Initialize the Ollama model
        self.llm = ChatOllama(
            model="phi3:3.8b",
            temperature=0
        )

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
            SystemMessage(content="""You are an answer verification expert. 
            Compare the user's answer with the correct answer and determine if they are semantically equivalent.
            You will accept answers that include misspellings and grammar problems. Rather than determining
            if the answer exactly matches the answer from the trivia database, you will act
            like a human trivia gameshow host and be flexible on some variance on the answer.
            Respond with only 'True' if correct or 'False' if incorrect."""),
            HumanMessage(content=f"""
            Correct answer: {correct_answer}
            User's answer: {user_answer}
            Are these answers semantically equivalent?
            """)
        ])

        response = self.llm.invoke(prompt.format_messages())
        return 'true' in response.content.lower()

    def run(self):
        """Main interaction loop"""
        print("Welcome to the Quiz Chatbot!")

        while True:
            print("\nAvailable categories:")
            print(self.get_categories())

            # Get category selection
            selection = input(
                "\nPlease select a category number (or 'quit' to exit): ")

            if selection.lower() == 'quit':
                print("Thank you for playing!")
                break

            try:
                category_index = int(selection) - 1
                if 0 <= category_index < len(self.categories):
                    selected_category = self.categories[category_index]

                    # Get random question from category
                    question, answer = self.select_question(selected_category)
                    if question is None:
                        print("Error: No questions available in this category.")
                        continue

                    # Ask question and get user's answer
                    print(f"\nQuestion: {question}")
                    user_answer = input("Your answer: ")

                    # Verify answer
                    is_correct = self.verify_answer(user_answer, answer)

                    # Provide feedback
                    if is_correct:
                        print("Correct! Well done!")
                    else:
                        print(f"Incorrect. The correct answer was: {answer}")
                else:
                    print("Invalid category number. Please try again.")
            except ValueError:
                print("Please enter a valid number.")


def chat(message, history, chatbot_instance):
    """
    Handle chat interactions for the quiz game.
    """
    # Initial greeting - this will show when the interface first loads
    if not history:
        categories = chatbot_instance.get_categories()
        return f"Welcome to the Quiz Game! 🎮\n\nPlease select a category by entering its number:\n\n{categories}"

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
                        return "Error: No questions available in this category. Please select another category:\n\n" + chatbot_instance.get_categories()

                    chatbot_instance.current_question = question
                    chatbot_instance.current_answer = answer

                    return f"Category: {selected_category}\n\nQuestion: {question}"
                else:
                    return f"Please select a valid category number between 1 and {len(chatbot_instance.categories)}:\n\n{chatbot_instance.get_categories()}"
            except ValueError:
                return f"Please enter a valid category number:\n\n{chatbot_instance.get_categories()}"

        # If there is a current question, treat the input as an answer
        else:
            is_correct = chatbot_instance.verify_answer(
                message, chatbot_instance.current_answer)
            response = (
                "🎉 Correct! Well done!"
                if is_correct
                else f"❌ Incorrect. The correct answer was: {chatbot_instance.current_answer}"
            )

            # Reset for next question
            chatbot_instance.current_question = None
            chatbot_instance.current_answer = None

            return f"{response}\n\nWould you like to try another question?\nSelect a category:\n\n{chatbot_instance.get_categories()}"

    except Exception as e:
        return f"An error occurred. Please try again.\n\n{chatbot_instance.get_categories()}"


def create_chatbot_interface():
    chatbot_instance = QuizChatbot("trivia_qa.db")

    iface = gr.ChatInterface(
        fn=lambda message, history: chat(message, history, chatbot_instance),
        title="🎯 Trivia Quiz Game",
        description="Test your knowledge with trivia questions! Select a category and answer questions.",
        examples=[{"text": "Start game"}],
        # retry_btn=None,
        # undo_btn="Previous",
        # clear_btn="Start Over",
        theme="soft",
        chatbot=gr.Chatbot(
            height=500,
            bubble_full_width=False,
        ),
        textbox=gr.Textbox(
            placeholder="Enter category number or your answer",
            container=False,
            scale=7
        ),
    )

    return iface


# Launch the interface
if __name__ == "__main__":
    iface = create_chatbot_interface()
    iface.launch()
