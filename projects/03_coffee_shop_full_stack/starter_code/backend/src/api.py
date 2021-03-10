import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', '*')
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8100')
    return response


'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''


# db_drop_and_create_all()

## ROUTES
@app.route('/drinks')
def get_drinks():
    drinks = [drink.short() for drink in Drink.query.all()]

    return jsonify({
        'success': True,
        'drinks': drinks
    })


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(jwt):
    try:
        drinks = [drink.long() for drink in Drink.query.all()]
    except AuthError:
        abort(401)

    return jsonify({
        'success': True,
        'drinks': drinks
    })


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(jwt):
    body = request.get_json()

    drink = Drink(
        title=body['title'],
        recipe=json.dumps(body['recipe'])
    )

    try:
        if body['title'] == '' or len(body['recipe']) == 0:
            abort(400)

        drink.insert()
    except():
        abort(422)

    return jsonify({
        'success': True,
        'drink': drink.id
    }, 200)


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(jwt, drink_id):
    body = request.get_json()

    drink = Drink.query.filter_by(id=drink_id).one_or_none()
    if drink is None:
        abort(404)

    try:
        if body['title'] == '' or len(body['recipe']) == 0:
            abort(400)

        drink.title = body['title']
        drink.recipe = json.dumps(body['recipe'])
        drink.update()

    except():
        abort(422)

    return jsonify({
        'success': True,
        'drink': drink.id
    })


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt, drink_id):
    drink = Drink.query.filter_by(id=drink_id).one_or_none()
    if drink is None:
        abort(404)

    try:
        drink.delete()

    except():
        abort(422)

    return jsonify({
        'success': True,
        'delete': drink.id
    })


## Error Handling
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(401)
def auth_error(error):
    message = "not authorized"
    if error.description:
        message = error.description

    return jsonify({
        "success": False,
        "error": 401,
        "message": message
    }), 401
