from flask import Blueprint, jsonify
import json

learn = Blueprint('learn', __name__)

@learn.route('/lessons', methods=['GET'])
def get_lessons():
    with open('data/lessons.json') as f:
        lessons = json.load(f)
    return jsonify(lessons)
