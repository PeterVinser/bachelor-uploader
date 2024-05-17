from flask import jsonify
from app.services.splitter import split_to_chunks
import weaviate
import os
from app.services.knowledge_base import add_to_vector_db

def save_to_db(document_name, chunks):
    client = weaviate.connect_to_wcs(
        cluster_url=os.getenv('WEAVIATE_HOST'),
        auth_credentials=weaviate.auth.AuthApiKey(os.getenv('WEAVIATE_ADMIN_KEY')),
        headers={
            'X-OpenAI-Api-Key': os.getenv('OPENAI_API_KEY')
        }
    )

    chunks_collection = client.collections.get('BachelorDocumentChunk')

    uuids = []

    for chunk in chunks:
        chunk_object = {
            "documentName": document_name,
            "content": chunk
        }

        uuid = chunks_collection.data.insert(chunk_object)

        uuids.append(uuid)

    client.close()

    return uuids

def handle_add_documents(request):
    document_name, document_content = request.json['documentName'], request.json['documentContent']

    chunks = split_to_chunks(document_content)

    uuids = []

    for chunk in chunks:
        uuid = add_to_vector_db(chunk)

        uuids.append(uuid)
    
    return jsonify({"resultMessage": f"document {document_name} added"})