import weaviate
import os

def get_weaviate_client():
    return weaviate.connect_to_wcs(
        cluster_url=os.getenv('WEAVIATE_HOST'),
        auth_credentials=weaviate.auth.AuthApiKey(os.getenv('WEAVIATE_ADMIN_KEY')),
        headers={
            'X-OpenAI-Api-Key': os.getenv('OPENAI_API_KEY')
        }
    )

def add_to_vector_db(document_name, chunk):
    client = weaviate.connect_to_wcs(
        cluster_url=os.getenv('WEAVIATE_HOST'),
        auth_credentials=weaviate.auth.AuthApiKey(os.getenv('WEAVIATE_ADMIN_KEY')),
        headers={
            'X-OpenAI-Api-Key': os.getenv('OPENAI_API_KEY')
        }
    )

    chunks_collection = client.collections.get('BachelorDocumentChunk')

    chunk_object = {
        "documentName": document_name,
        "content": chunk
    }

    uuid = chunks_collection.data.insert(chunk_object)

    client.close()

    return uuid