import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}/{}".format('postgres','sapphire1!@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
                'question': 'What is the name of the song Beyonce and Wizkid sang?',
                'answer': 'Brown Skin Girl',
                'category': 5,
                'difficulty': 3,
                'rating':5
            }

        self.new_category = {
                'type': 'Technology'
            }
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

           
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_categories'])
        self.assertEqual(data['success'], True)

    def test_404_requesting_non_existing_category(self):
        res = self.client().get('/categories/9999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'Resource Not Found')
        self.assertEqual(data['success'], False)

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertEqual(data['success'], True)

    def test_404_requesting_questions_beyond_valid_page(self):
        res = self.client().get('/questions?page=10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'Resource Not Found')
        self.assertEqual(data['success'], False)

    def test_delete_question(self):
        res = self.client().delete('/questions/13')
        data = json.loads(res.data)
        self.assertEqual(data['deleted'], 13)
        self.assertEqual(data['success'], True)

    def test_422_deleting_non_existing_question(self):
        res = self.client().delete('/questions/200000000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['message'], 'Unprocessable')
        self.assertEqual(data['success'], False)

    def test_search_questions(self):
        res = self.client().post('/questions', json={'searchTerm': 'beyonce'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_question'])
        self.assertEqual(data['success'], True)

    def test_create_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['created'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(data["success"], True)
    
    def test_create_category(self):
        res = self.client().post('/categories', json=self.new_category)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])
        self.assertTrue(data['created'])
        self.assertTrue(data['total_categories'])
        self.assertEqual(data["success"], True)

    def test_search_question_without_results(self):
        res = self.client().post('/questions', json={'searchTerm':'*'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["total_question"], 0)
        self.assertEqual(data["success"], True)

    def test_get_questions_per_category(self):
        category_id = 5
        res = self.client().get(f'/categories/{category_id}/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['current_category'])
        self.assertEqual(data['success'], True)

    def test_404_get_questions_per_category(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["message"], "Resource Not Found")
        self.assertEqual(data["success"], False)

    def test_play_quiz(self):
        new_quiz_round = {'previous_questions': [],
                          'quiz_category': {'type': 'Entertainment', 'id': 5}}
        res = self.client().post('/play', json=new_quiz_round)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])
        self.assertEqual(data['success'], True)

    def test_422_play_quiz(self):
        new_quiz_round = {'previous_questions': []}
        res = self.client().post('/play', json=new_quiz_round)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["message"], "Unprocessable")
        self.assertEqual(data["success"], False)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()