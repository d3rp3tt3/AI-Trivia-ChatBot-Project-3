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

class UnitTestQuizChatbot(unittest.TestCase):
    """Run unit tests for the QuizChatbot class"""
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
        with open('unit_test_results.csv', 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['timestamp', 'test_name', 'iteration', 'result', 'details']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Check if the file is empty to write the header
            csvfile.seek(0, os.SEEK_END)
            if csvfile.tell() == 0:
                writer.writeheader()

            for result in cls.test_results:
                writer.writerow(result)

    def test_get_categories(self):
        """Test the get_categories method of the QuizChatbot"""
        for i in range(self.NUM_ITERATIONS):
            try:
                expected_categories = self.test_data['Category'].unique().tolist()
                categories = self.chatbot.get_categories().split('\n')
                self.assertEqual(len(categories), len(expected_categories))
                for j, category in enumerate(expected_categories):
                    self.assertIn(category, categories[j])
                self.test_results.append({
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'test_name': 'test_get_categories',
                    'iteration': i + 1,
                    'result': 'Pass',
                    'details': ''
                })
            except AssertionError as e:
                self.test_results.append({
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'test_name': 'test_get_categories',
                    'iteration': i + 1,
                    'result': 'Fail',
                    'details': str(e)
                })

    def test_select_question(self):
        """Test the select_question method of the QuizChatbot"""
        for i in range(self.NUM_ITERATIONS):
            try:
                category = 'SCIENCE'
                question, answer = self.chatbot.select_question(category)
                self.assertIn(
                    question, self.test_data[self.test_data['Category'] == category]['Question'].values)
                self.assertIn(
                    answer, self.test_data[self.test_data['Category'] == category]['Answer'].values)
                self.test_results.append({
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'test_name': 'test_select_question',
                    'iteration': i + 1,
                    'result': 'Pass',
                    'details': ''
                })
            except AssertionError as e:
                self.test_results.append({
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'test_name': 'test_select_question',
                    'iteration': i + 1,
                    'result': 'Fail',
                    'details': str(e)
                })

if __name__ == '__main__':
    unittest.main(verbosity=2)
