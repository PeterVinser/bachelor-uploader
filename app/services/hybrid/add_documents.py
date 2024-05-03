from flask import jsonify
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings
import weaviate
import os

def handle_documents(request):
    document_name, document_content = request.json['documentName'], request.json['documentContent']
    
    return jsonify({"resultMessage": f"document {document_name} added"})