import unittest
import sqlite3
import pandas as pd
import sys
import os
import csv
from unittest.mock import patch
from datetime import datetime
from local_quizchatbot import QuizChatbot

# Add the current directory to the system path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

class TestQuizChatbot(unittest.TestCase):
    """Test the QuizChatbot class"""
    NUM_ITERATIONS = 5  # Define the number of times each test should run
    test_results = []  # List to store test results

    @classmethod
    def setUpClass(cls):
        # Initialize the QuizChatbot with the test database
        cls.chatbot = QuizChatbot('testing_trivia_qa.db')

        # Load test data from the SQLite database
        conn = sqlite3.connect('testing_trivia_qa.db')
        cls.test_data = pd.read_sql_query("SELECT * FROM jeopardy", conn)
        conn.close()

    @classmethod
    def tearDownClass(cls):
        # Write test results to a CSV file
        with open('functional_test_results.csv', 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['timestamp', 'test_name', 'iteration', 'question', 'correct_answer', 'human_answer', 'llm_result', 'result', 'details']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Check if the file is empty to write the header
            csvfile.seek(0, os.SEEK_END)
            if csvfile.tell() == 0:
                writer.writeheader()

            for result in cls.test_results:
                writer.writerow(result)

    @patch('local_quizchatbot.ChatOllama.invoke')
    def test_verify_answer_correct(self, mock_invoke):
        """Test the verify_answer method of the QuizChatbot with correct answers"""
        for i in range(self.NUM_ITERATIONS):
            try:
                # Mock the response of the LLM
                mock_invoke.return_value.content = 'True'
                example_row = self.test_data.sample(n=1).iloc[0]
                user_answer = example_row['MockHumanAnswer']
                correct_answer = example_row['Answer']
                result = self.chatbot.verify_answer(user_answer, correct_answer)
                self.assertTrue(result)
                self.test_results.append({
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'test_name': 'test_verify_answer_correct',
                    'iteration': i + 1,
                    'question': example_row['Question'],
                    'correct_answer': correct_answer,
                    'human_answer': user_answer,
                    'llm_result': result,
                    'result': 'Pass',
                    'details': ''
                })
            except AssertionError as e:
                self.test_results.append({
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'test_name': 'test_verify_answer_correct',
                    'iteration': i + 1,
                    'question': example_row['Question'],
                    'correct_answer': correct_answer,
                    'human_answer': user_answer,
                    'llm_result': result,
                    'result': 'Fail',
                    'details': str(e)
                })

    @patch('local_quizchatbot.ChatOllama.invoke')
    def test_verify_answer_incorrect(self, mock_invoke):
        """Test the verify_answer method of the QuizChatbot with incorrect answers"""
        for i in range(self.NUM_ITERATIONS):
            try:
                # Mock the response of the LLM
                mock_invoke.return_value.content = 'False'
                example_row = self.test_data.sample(n=1).iloc[0]
                user_answer = example_row['MockHumanAnswer']
                correct_answer = example_row['Answer']
                result = self.chatbot.verify_answer(user_answer, correct_answer)
                self.assertFalse(result)
                self.test_results.append({
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'test_name': 'test_verify_answer_incorrect',
                    'iteration': i + 1,
                    'question': example_row['Question'],
                    'correct_answer': correct_answer,
                    'human_answer': user_answer,
                    'llm_result': result,
                    'result': 'Pass',
                    'details': ''
                })
            except AssertionError as e:
                self.test_results.append({
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'test_name': 'test_verify_answer_incorrect',
                    'iteration': i + 1,
                    'question': example_row['Question'],
                    'correct_answer': correct_answer,
                    'human_answer': user_answer,
                    'llm_result': result,
                    'result': 'Fail',
                    'details': str(e)
                })

if __name__ == '__main__':
    unittest.main(verbosity=2)
