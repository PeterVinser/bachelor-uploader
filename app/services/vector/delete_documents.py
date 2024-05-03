from flask import jsonify
import weaviate
import weaviate.classes as wvc
import os

def handle_delete_document(request):
    document_name = request.json['documentName']

    client = weaviate.connect_to_wcs(
        cluster_url=os.getenv('WEAVIATE_HOST'),
        auth_credentials=weaviate.auth.AuthApiKey(os.getenv('WEAVIATE_ADMIN_KEY')),
    )

    chunks_collection = client.collections.get('BachelorDocumentChunk')

    response = chunks_collection.query.fetch_objects(
        filters=wvc.query.Filter.by_property("documentName").equal(document_name)
    )

    for o in response.objects:
        chunks_collection.data.delete_by_id(o.uuid)
    
    client.close()

    return jsonify({"resultMessage": f"document {document_name} deleted"})