from flask import jsonify
from app.services.splitter import split_to_chunks
from app.services.vector_store import VectorStore

def handle_add_documents(request):
    document_name, document_content = request.json['documentName'], request.json['documentContent']

    chunks = split_to_chunks(document_content)

    with VectorStore() as store:
        store.add_document_chunks(document_name, chunks)
    
    return jsonify({"resultMessage": f"document {document_name} added"})