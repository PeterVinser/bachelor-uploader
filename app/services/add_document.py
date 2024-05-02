from flask import jsonify
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

def handle_add_document(request):
    document_name = request.json['documentName']
    document_content = request.json['documentContent']

    text_splitter = SemanticChunker(OpenAIEmbeddings())
    
    chunks = text_splitter.create_documents([document_content])
    
    return jsonify({"result": "success", "name": document_name, "chunks": [c.page_content for c in chunks]})