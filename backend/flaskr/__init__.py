import os
from unicodedata import category
from flask import Flask, current_app, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page-1)* QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODO(done)
    """
    CORS(app, resources={'/': {'origins':'*'}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow (DONE)
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, DELETE, POST, OPTIONS')
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.(done)
    """
    @app.route("/categories", methods=['GET'])
    def list_categories():
        categories = {}
        for category in Category.query.all():
            categories[category.id] = category.type

        if len(categories) == 0:
            abort(404)

        return jsonify(
            {
                "categories": categories,
                "total_categories": len(categories),
                "success": True
            }
        )

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. (done)
    """
    @app.route("/questions", methods=['GET'])
    def list_questions():
        selection = Question.query.order_by(Question.id).all()
        categories = {}
        for category in Category.query.all():
            categories[category.id] = category.type
        current_questions = paginate_questions(request, selection)

        if len(current_questions) == 0:
            abort(404)

        return jsonify(
            {
                "questions": current_questions,
                "total_questions": len(Question.query.all()),
                "categories": categories,
                "success": True
            }
        )
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.(done)
    """
    @app.route("/questions/<int:question_id>", methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            if not question:
                abort(404)

            question.delete()    
            return jsonify(
                    {
                        "deleted": question_id,
                        "success": True
                    }
                )
        except:
            abort(422)
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.(done)
    """
    @app.route("/questions", methods=['POST'])
    def create_question():
        body = request.get_json()

        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_category = body.get("category", None)
        new_difficulty = body.get("difficulty", None)
        new_rating = body.get("rating", None)
        searchTerm = body.get('searchTerm')
        
        try:
            if searchTerm:
                result = Question.query.order_by(Question.id).filter(Question.question.ilike(f'%{searchTerm}%')).all()
                current_questions= paginate_questions(request, result)
                return jsonify({
                    'questions': current_questions,
                    'total_question': len(result),
                    'success':True
                })
            else:
                question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty, rating=new_rating)
                question.insert()

                selection = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, selection)

                return jsonify(
                    {
                        "questions": current_questions,
                        "created": question.id,
                        "total_questions": len(Question.query.all()),
                        "success": True
                    }
                )
        except:
            abort(422)
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.(done)
    """
    """
    @BONUS:
    Create a POST endpoint to create a new category(done)
    """
    @app.route("/categories", methods=['POST'])
    def create_category():
        body = request.get_json()

        new_type = body.get("type", None)
        
        try:
            category = Category(type=new_type)
            category.insert()

            selection = Category.query.order_by(Category.id).all()
            categories = [category.format() for category in selection]

            return jsonify(
                    {
                        "categories": categories,
                        "created": category.id,
                        "total_categories": len(categories),
                        "success": True
                    }
                )
        except:
            abort(422)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.(done)
    """
    @app.route("/categories/<int:category_id>/questions", methods=['GET'])
    def list_category_questions(category_id):
        category = Category.query.filter(category_id == Category.id).one_or_none()

        if (category is None):
            abort(404)
        else:
            try:
                selection = Question.query.filter(Question.category == category.id).all()
                current_questions = paginate_questions(request, selection)

                return jsonify({
                    'questions': current_questions,
                    'current_category': category.type,
                    'total_questions': len(selection),
                    'success': True
                })

            except:
                abort(404)
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.(done)
    """
    @app.route("/play", methods=['POST'])
    def play_trivia():
        try:
            body = request.get_json()
            if not('quiz_category' in body and 'previous_questions' in body):
                abort(422)
            quiz_category = body.get('quiz_category')
            category_id = quiz_category['id']
            previous_questions = body.get('previous_questions')
            if category_id == 0:
                questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
            else:
                questions = Question.query.filter(Question.id.notin_(previous_questions), Question.category == category_id).all()
            if(questions):
                question = random.choice(questions)
            return jsonify({
                'question': question.format(),
                'success': True
            })
        except:
            abort(422)
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422. (done)
    """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'error':400,
            'message': 'Bad Request',
            'success': False
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error':404,
            'message': 'Resource Not Found',
            'success': False
        }), 404
    
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'error':422,
            'message': 'Unprocessable',
            'success': False
        }), 422
    
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'error':500,
            'message': 'Internal Server Error',
            'success': False
        }), 500

    return app

