from flask import Blueprint, request, jsonify
from app.services.add_document import handle_add_document
from app.services.delete_document import handle_delete_document

api_blueprint = Blueprint('api', __name__)

RAG_TYPES = ['vector', 'graph', 'hybrid']

@api_blueprint.route('/add/<type>', methods=['POST'])
def add(type):
    if type not in RAG_TYPES:
        return jsonify({"error": "Invalid RAG type"}), 400

    return handle_add_document(type, request)

@api_blueprint.route('/delete/<type>', methods=['POST'])
def delete(type):
    if type not in RAG_TYPES:
        return jsonify({"error": "Invalid RAG type"}), 400

    return handle_delete_document(type, request)