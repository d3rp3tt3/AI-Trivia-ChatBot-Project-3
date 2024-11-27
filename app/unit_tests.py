from local_quizchatbot import QuizChatbot
import unittest
import sqlite3
import pandas as pd
import sys
import os
from unittest.mock import patch

# Add the current directory to the system path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


class TestQuizChatbot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize the QuizChatbot with the test database
        cls.chatbot = QuizChatbot('testing_trivia_qa.db')

        # Load test data from the SQLite database
        conn = sqlite3.connect('testing_trivia_qa.db')
        cls.test_data = pd.read_sql_query("SELECT * FROM jeopardy", conn)
        conn.close()

    def test_get_categories(self):
        expected_categories = self.test_data['Category'].unique().tolist()
        categories = self.chatbot.get_categories().split('\n')
        self.assertEqual(len(categories), len(expected_categories))
        for i, category in enumerate(expected_categories):
            self.assertIn(category, categories[i])

    def test_select_question(self):
        category = 'SCIENCE'
        question, answer = self.chatbot.select_question(category)
        self.assertIn(
            question, self.test_data[self.test_data['Category'] == category]['Question'].values)
        self.assertIn(
            answer, self.test_data[self.test_data['Category'] == category]['Answer'].values)

    @patch('local_quizchatbot.ChatOllama.invoke')
    def test_verify_answer_correct(self, mock_invoke):
        # Mock the response of the LLM
        mock_invoke.return_value.content = 'True'
        user_answer = 'sound'
        correct_answer = 'sound'
        self.assertTrue(self.chatbot.verify_answer(
            user_answer, correct_answer))

    @patch('local_quizchatbot.ChatOllama.invoke')
    def test_verify_answer_incorrect(self, mock_invoke):
        # Mock the response of the LLM
        mock_invoke.return_value.content = 'False'
        user_answer = 'light'
        correct_answer = 'sound'
        self.assertFalse(self.chatbot.verify_answer(
            user_answer, correct_answer))


if __name__ == '__main__':
    unittest.main(verbosity=2)
