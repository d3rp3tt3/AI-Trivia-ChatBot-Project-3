import pandas as pd
import unittest
from local_quizchatbot import QuizChatbot
import sys
import os


class TestQuizChatbot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load test data
        cls.test_data = pd.read_csv('test_data.csv')
        cls.chatbot = QuizChatbot('test_data.csv')

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

    def test_verify_answer_correct(self):
        user_answer = 'sound'
        correct_answer = 'sound'
        self.assertTrue(self.chatbot.verify_answer(
            user_answer, correct_answer))

    def test_verify_answer_incorrect(self):
        user_answer = 'light'
        correct_answer = 'sound'
        self.assertFalse(self.chatbot.verify_answer(
            user_answer, correct_answer))


if __name__ == '__main__':
    unittest.main()
