import weaviate
import os

class VectorStore:
    def __init__(self) -> None:
        self.client = weaviate.connect_to_wcs(
            cluster_url=os.getenv('WEAVIATE_HOST'),
            auth_credentials=weaviate.auth.AuthApiKey(os.getenv('WEAVIATE_ADMIN_KEY')),
            headers={
                'X-OpenAI-Api-Key': os.getenv('OPENAI_API_KEY')
            }
        )

        self.chunk_collection = self.client.collections.get('BachelorDocumentChunk')
        self.entity_collection = self.client.collections.get('BachelorEntity')

    def close(self) -> None:
        self.client.close()

    def __enter__(self) -> 'VectorStore':
        return self
    
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()

    def add_document_chunks(self, document_name, chunks):

        for chunk in chunks:
            chunk_object = {
                "documentName": document_name,
                "content": chunk
            }

            _ = self.chunk_collection.data.insert(chunk_object)

    def _entity_exists(self, entity_id):
        result = self.entity_collection.query.fetch_objects(
            filters=weaviate.classes.query.Filter.by_property("entityId").equal(entity_id)
        )

        return len(result.objects) > 0

    def add_entity(self, entity):
        if not self._entity_exists(entity.id):
            entity_object = {
                "entityId": entity.id,
                "entityType": entity.type
            }

            _ = self.entity_collection.data.insert(entity_object)

