from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import setup_db, Question, Category
from sqlalchemy import and_
import sys
import random

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, all_questions):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in all_questions]

    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is not None:
        app.config.from_object(test_config)
    else:
        app.config.from_object('config.DevelopmentConfig')

    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories')
    def retrieve_categories():
        categories = [category.format() for category in Category.query.order_by('id').all()]

        if len(categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': categories
        })

    @app.route('/categories/<int:category_id>/questions')
    def retrieve_questions_per_category(category_id):
        questions = Question.query.filter_by(category=category_id).all()
        current_questions = paginate_questions(request, questions)
        current_category = Category.query.filter_by(id=category_id).one_or_none()

        if current_category is None:
            abort(400)

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(questions),
            'current_category': current_category.format()
        })

    @app.route('/categories/<int:category_id>/questions', methods=['POST'])
    def search_questions_per_category(category_id):
        body = request.get_json()
        search = body.get('searchTerm', None)
        selection = Question.query\
            .order_by(Question.id)\
            .filter(and_(Question.question.ilike('%{}%'.format(search)),
                         Question.category == category_id)).all()
        current_questions = paginate_questions(request, selection)
        current_category = Category.query.filter_by(id=category_id).one_or_none()

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'current_category': current_category.format()
        })

    @app.route('/questions')
    def retrieve_questions():
        all_questions = Question.query.order_by('id').all()
        current_questions = paginate_questions(request, all_questions)
        categories = [category.format() for category in Category.query.order_by('id').all()]

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(all_questions),
            'categories': [category for category in categories]
        })

    @app.route('/questions', methods=['POST'])
    def create_or_search_question():
        body = request.get_json()
        search = body.get('searchTerm', None)

        if search is None:
            question = body.get('question')
            answer = body.get('answer')
            category = body.get('category')
            difficulty = body.get('difficulty')

            try:
                if question == '' or answer == '':
                    abort(400)

                question = Question(
                    question=question,
                    answer=answer,
                    category=category,
                    difficulty=difficulty
                )
                question.insert()

                all_questions = Question.query.order_by('id').all()
                current_questions = paginate_questions(request, all_questions)

                return jsonify({
                    'success': True,
                    'created': question.id,
                    'current_questions': current_questions,
                    'total_questions': len(all_questions)
                })

            except():
                print(sys.exc_info())
                abort(422)

        else:
            try:
                selection = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search)))
                current_questions = paginate_questions(request, selection)

                return jsonify({
                    'success': True,
                    'questions': current_questions,
                    'total_questions': len(selection.all())
                })

            except():
                print(sys.exc_info())
                abort(422)

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()

            return jsonify({
                'success': True,
                'deleted': question_id
            })

        except():
            abort(422)

    @app.route('/quizzes', methods=['POST'])
    def return_quiz():
        body = request.get_json()
        previous_questions = body.get('previous_questions')
        quiz_category = body.get('quiz_category')
        all_questions = [question.format() for question in Question.query.all()]

        if quiz_category is not None:
            all_questions = [question.format() for question in
                             Question.query.filter_by(category=quiz_category['id']).all()]

        if len(all_questions) == 0:
            abort(404)

        choices = []

        for choice in all_questions:
            if previous_questions:
                if choice['id'] not in previous_questions:
                    choices.append(choice)
            else:
                choices.append(choice)

        random.shuffle(choices)
        previous_questions.append(choices[0]['id'])

        return jsonify({
            'success': True,
            'question': choices[0],
            'previous_questions': previous_questions
        })

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    return app
