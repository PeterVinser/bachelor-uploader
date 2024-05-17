from flask import jsonify
from langchain_openai import ChatOpenAI
from langchain_community.graphs.neo4j_graph import Neo4jGraph
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_core.documents import Document
from app.services.splitter import split_to_chunks
import weaviate
import uuid
from app.services.knowledge_base import get_weaviate_client

def add_node_to_weaviate(collection, node):
    already_exists = collection.query.fetch_objects(
        filters=weaviate.classes.query.Filter.by_property("entityId").equal(node.id)
    )

    if len(already_exists.objects) == 0:
        entity_object = {
            "entityId": node.id,
            "entityType": node.type
        }

        collection.data.insert(entity_object)

def add_chunk_to_graph(graph, chunk, chunk_id):
    graph.query(
        "CREATE (d:DocumentChunk {content: $content, id: $id})",
        params={"content": chunk, "id": str(chunk_id)}
    )

def link_node_with_chunk(graph, node, chunk_id):
    graph.query(
        f"MATCH (e:{node.type} {{id: $id}}), (d:DocumentChunk {{id: $chunk_id}}) CREATE (e)-[:EXTRACTED_FROM]->(d)",
        params={"id": node.id, "chunk_id": str(chunk_id)}
    )

def add_chunk_to_db(graph, collection, llm_transformer, chunk):
        chunk_id = uuid.uuid4()

        add_chunk_to_graph(graph, chunk, chunk_id)

        graph_documents = llm_transformer.convert_to_graph_documents([Document(page_content=chunk)])

        graph.add_graph_documents(graph_documents)

        for doc in graph_documents:
            for node in doc.nodes:
                add_node_to_weaviate(collection, node)
                link_node_with_chunk(graph, node, chunk_id)
    

def handle_documents(request):
    document_name, document_content = request.json['documentName'], request.json['documentContent']

    chunks = split_to_chunks(document_content)

    llm = ChatOpenAI(temperature=0, model="gpt-4o")

    llm_transformer = LLMGraphTransformer(llm=llm)

    graph = Neo4jGraph()

    client = get_weaviate_client()

    entities_collection = client.collections.get("BachelorEntity")

    for chunk in chunks:
        if chunk == '':
            continue

        add_chunk_to_db(graph, entities_collection, llm_transformer, chunk)

    client.close()

    return jsonify({"resultMessage": f"document {document_name} added"})