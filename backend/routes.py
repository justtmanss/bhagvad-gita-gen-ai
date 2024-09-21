from flask import Blueprint, jsonify
from models import Chapter, Sloka

api_bp = Blueprint('api', __name__)

@api_bp.route('/chapters', methods=['GET'])
def get_chapters():
    chapters = Chapter.query.all()
    return jsonify([{'id': chapter.id, 'title': chapter.title} for chapter in chapters])

@api_bp.route('/slokas/<int:chapter_id>', methods=['GET'])
def get_slokas_by_chapter(chapter_id):
    slokas = Sloka.query.filter_by(chapter_id=chapter_id).all()
    return jsonify([{'id': sloka.id, 'text': sloka.text} for sloka in slokas])
