import os
import sys

topdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(topdir)

import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app, jsonify
from models import setup_db, Question, Category


class AppTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(test_config='config.TestingConfig')
        self.client = self.app.test_client

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy(self.app)
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def load_fixture(self, path, class_):
        s = self.db.session()
        file = open(path, 'r')
        fixture = json.load(file)

        file.close()
        self.db.session.execute(f'ALTER SEQUENCE {class_.__table__}_id_seq RESTART WITH 1')

        for data in fixture:
            instance = class_(**data)
            s.add(instance)

        s.commit()

    def remove_fixture(self, class_):
        s = self.db.session()
        s.query(class_).delete()
        s.commit()

    def tearDown(self):
        self.remove_fixture(Question)
        self.remove_fixture(Category)
        self.db.session.remove()
        pass

    def test_retrieve_categories(self):
        """Test get categories endpoint"""
        self.load_fixture('tests/fixtures/categories.json', Category)

        res = self.client().get('/categories')
        data = json.loads(res.get_data(as_text=True))

        self.assertTrue(data['success'])
        self.assertTrue(data['categories'])

    def test_retrieve_categories_404_error(self):
        """Test get categories endpoint 404 error"""

        res = self.client().get('/categories')
        data = json.loads(res.get_data(as_text=True))

        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)

    def test_retrieve_questions(self):
        """Test get questions endpoint"""
        self.load_fixture('tests/fixtures/questions.json', Question)
        self.load_fixture('tests/fixtures/categories.json', Category)

        questions = Question.query.all()

        res = self.client().get('/questions')
        data = json.loads(res.get_data(as_text=True))

        self.assertTrue(data['success'])
        self.assertEqual(len(data['questions']), 10)
        self.assertEqual(data['total_questions'], len(questions))
        self.assertTrue(data['categories'])

    def test_retrieve_questions_next_page(self):
        """Test get questions endpoint with page parameter"""
        self.load_fixture('tests/fixtures/questions.json', Question)
        self.load_fixture('tests/fixtures/categories.json', Category)

        questions = Question.query.all()

        res = self.client().get('/questions?page=3')
        data = json.loads(res.get_data(as_text=True))

        self.assertTrue(data['success'])
        self.assertEqual(len(data['questions']), len(questions) % 10)
        self.assertEqual(data['total_questions'], len(questions))
        self.assertTrue(data['categories'])

    def test_retrieve_questions_404_error(self):
        """Test get questions endpoint with page parameter"""
        self.load_fixture('tests/fixtures/categories.json', Category)

        res = self.client().get('/questions?page=3')
        data = json.loads(res.get_data(as_text=True))

        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)

    def test_get_questions_per_category(self):
        """Test get questions for a specific category endpoint"""
        self.load_fixture('tests/fixtures/questions.json', Question)
        self.load_fixture('tests/fixtures/categories.json', Category)

        questions = Question.query.filter_by(category=1).all()

        res = self.client().get('/categories/1/questions')
        data = json.loads(res.get_data(as_text=True))

        self.assertTrue(data['success'])
        self.assertEqual(len(data['questions']), len(questions))
        self.assertEqual(data['total_questions'], len(questions))
        self.assertEqual(data['current_category']['id'], 1)
        self.assertEqual(data['current_category']['type'], 'Science')

    def test_create_new_question(self):
        """Test creating a new question"""
        self.load_fixture('tests/fixtures/questions.json', Question)

        questions = Question.query.all()

        new_question = {
            'question': 'What is the most populous city in the world?',
            'answer': 'Tokyo',
            'difficulty': 2,
            'category': 3
        }

        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.get_data(as_text=True))

        self.assertTrue(data['success'])
        self.assertTrue(['current_questions'])
        self.assertEqual(data['total_questions'], len(questions)+1)
        self.assertEqual(data['created'], 23)

    def test_create_new_question_no_question_error(self):
        """Test error response when attempting to create a new question
        without sending the question in the request"""
        self.load_fixture('tests/fixtures/questions.json', Question)

        new_question = {
            'question': '',
            'answer': 'Marie Curie',
            'category': 1,
            'difficulty': 1
        }

        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.get_data(as_text=True))

        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 400)

    def test_create_new_question_no_answer_error(self):
        """Test error response when attempting to create a new question
        without sending the answer in the request"""
        self.load_fixture('tests/fixtures/questions.json', Question)

        new_question = {
            'question': 'What is the most populous city in the world?',
            'answer': '',
            'category': 3,
            'difficulty': 1
        }

        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.get_data(as_text=True))

        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 400)


if __name__ == "__main__":
    unittest.main()
