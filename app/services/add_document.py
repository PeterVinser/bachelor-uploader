from flask import jsonify
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings
import weaviate
import os

def split_to_chunks(document_content):
    text_splitter = SemanticChunker(OpenAIEmbeddings())
    
    chunks = text_splitter.create_documents([document_content])

    return [chunk.page_content for chunk in chunks]

def save_to_db(document_name, chunks):
    client = weaviate.connect_to_wcs(
        cluster_url=os.getenv('WEAVIATE_HOST'),
        auth_credentials=weaviate.auth.AuthApiKey(os.getenv('WEAVIATE_ADMIN_KEY')),
        headers={
            'X-OpenAI-Api-Key': os.getenv('OPENAI_API_KEY')
        }
    )

    db_chunks = client.collections.get('BachelorDocumentChunk')

    uuids = []

    for chunk in chunks:
        chunk_object = {
            "documentName": document_name,
            "content": chunk
        }

        uuid = db_chunks.data.insert(chunk_object)

        uuids.append(uuid)

    client.close()

    return uuids


def handle_add_document(request):
    document_name, document_content = request.json['documentName'], request.json['documentContent']

    chunks = split_to_chunks(document_content)

    uuids = save_to_db(document_name, chunks)
    
    return jsonify({"resultMessage": "success"})