import gradio as gr
import pandas as pd
from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain.schema import HumanMessage, SystemMessage
import random
import sqlite3
import getpass
from getpass import getpass
import os
from langchain_huggingface import HuggingFaceEndpoint
from langchain_mistralai import ChatMistralAI
from langchain_core.output_parsers import StrOutputParser

class QuizChatbot:
    def __init__(self, db_path: str):
        # Connect to the SQLite database
        conn = sqlite3.connect('trivia_qa.db')

        # Execute a query to retrieve the data
        query = "SELECT * FROM jeopardy"
        self.df = pd.read_sql_query(query, conn)

        # Close the connection
        conn.close()

        self.categories = self.df['Category'].unique().tolist()
		
        #if "MISTRAL_API_KEY" not in os.environ:
        #api_key = os.getenv("MISTRAL_API_KEY")
        #os.environ["MISTRAL_API_KEY"] = api_key 
            
        # Initialize the Ollama model for question answering
        self.llm = HuggingFaceEndpoint(
            repo_id="mistralai/Mistral-7B-Instruct-v0.3",
            max_new_tokens=256,
            temperature=0.7,
            token = os.getenv("UNCProjectToken")
        )
        
        # Initialize LLM for fallback responses
        self.fallback_llm = HuggingFaceEndpoint(
            repo_id="mistralai/Mistral-7B-Instruct-v0.3",
            max_new_tokens=256,
            temperature=1,
            token = os.getenv("UNCProjectToken")
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

    def verify_answer(self, user_answer: str, correct_answer: str) -> dict:
        """Use the LLM to verify if the answer is correct or close"""
        system_message = """You are a trivia gameshow host for a question and answer style trivia game. 
            Compare the user's answer with the correct answer and determine if they are:
            1. Exact match
            2. Close match (semantically similar but not identical, and this can include typos or a partial match)
            3. Not a match

            Return one of the following strings:
            'exact_match'
            'close_match'
            'not_a_match'."""
        
        user_text = f"""Correct answer: {correct_answer} User's answer: {user_answer} How do these answers compare? """
        
        prompt = PromptTemplate.from_template(
            (
                "[INST] {system_message}"
                "\nUser: {user_text}.\n [/INST]"
            )
        )

        chat = prompt | self.llm.bind(skip_prompt=True) | StrOutputParser(output_key='content')
    
        # Generate the response
        response = chat.invoke(input=dict(system_message=system_message, user_text=user_text))
        
        comparison_result = response #.content.strip().lower()
        
        return {
            'result': comparison_result,
            'user_answer': user_answer,
            'correct_answer': correct_answer
            }
        
    def get_additional_info(self, question: str) -> str:
        """Generate additional information about the topic of the question"""
        #prompt = ChatPromptTemplate.from_messages([
        #    SystemMessage(content="""You are an informative assistant for a trivia game. Given a question, generate a short paragraph (about 50-75 words) providing interesting facts or background information related to the topic of the question. Avoid repeating any information directly from the question itself."""),
        #    HumanMessage(content=f"Question: {question}")
        #])

        system_message = "You are an informative assistant for a trivia game. Given a question, generate a short paragraph (about 50-75 words) providing interesting facts or background information related to the topic of the question. Avoid repeating any information directly from the question itself."
        user_text = f"Question: {question}"
                
        prompt = PromptTemplate.from_template(
            (
                "[INST] {system_message}"
                "\nUser: {user_text}.\n [/INST]"
            )
        )
        
        chat = prompt | self.llm.bind(skip_prompt=True) | StrOutputParser(output_key='content')

        # Generate the response
        response = chat.invoke(input=dict(system_message=system_message, user_text=user_text))

        return response
        
def friendly_fallback_response(chatbot_instance):
    """
    Generate a friendly fallback response using an LLM.
    """   
    # Define prompt template for fallback responses
    system_message = """You are a friendly and succinct assistant for a trivia game chatbot. 
    Generate a helpful and encouraging message when unexpected input occurs. Include the following elements in your response:
    1. Let the user know you don't understand
    2. Write the user a short poem
    3. Tell the user to select a category to play the game
    4. End with an encouraging statement
    Keep the message no longer than 4 sentences."""

    user_text = f"Unexpected input occurred. {chatbot_instance.current_answer}"

    prompt = PromptTemplate.from_template(
        (
            "[INST] {system_message}"
            "\nUser: {user_text}.\n [/INST]"
            )
        )
    
    try:               
        chat = prompt | chatbot_instance.fallback_llm.bind(skip_prompt=True) | StrOutputParser(output_key='content')

        # Generate the response
        response = chat.invoke(input=dict(system_message=system_message, user_text=user_text))
        return f"{response}\n\nAvailable categories:\n{chatbot_instance.get_categories()}"        
    except Exception as e:
        # Fallback to static message if LLM fails        
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
            verification_result = chatbot_instance.verify_answer(message, chatbot_instance.current_answer)
            
            if verification_result['result'] == 'exact_match':
                response = "🎉 Correct! Well done!"
            elif verification_result['result'] == 'close_match':
                response = f"""Close! Your answer '{verification_result['user_answer']}' was very good, but the exact answer was '{
                    verification_result['correct_answer']}'. Great job!"""
            else:
                response = f"""Sorry, that wasn't quite right. The correct answer was: {verification_result['correct_answer']}"""

            additional_info = chatbot_instance.get_additional_info(
                chatbot_instance.current_question)
            
            # Reset for next question
            chatbot_instance.current_question = None
            chatbot_instance.current_answer = None

            return f"{response}\n\nAdditional info:\n{additional_info}\n\nWould you like to try another question?\nSelect a category:\n\n{chatbot_instance.get_categories()}"

    except Exception as e:
        return friendly_fallback_response(chatbot_instance)
        #return f"Error:{e}"


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
