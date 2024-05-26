from flask import jsonify
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.graphs.neo4j_graph import Neo4jGraph
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_core.documents import Document
from app.services.splitter import split_to_chunks
import uuid
from app.services.vector_store import VectorStore
from app.services.graph_store import GraphStore, extraction_prompt
import os

def add_relation_embeddings(graph_documents):
    for doc in graph_documents:
        embeddings = OpenAIEmbeddings()

        for relation in doc.relationships:
            type_embedding = embeddings.embed_query(relation.type)
            relation.properties['embedding'] = type_embedding

def add_chunk_to_db(graph, llm_transformer, chunk):
        chunk_id = uuid.uuid4()

        with GraphStore(uri=os.getenv("NEO4J_HYBRID_URI"), password=os.getenv("NEO4J_HYBRID_PASSWORD")) as graph_store:
            graph_store.add_chunk(chunk_id, chunk)

        graph_documents = llm_transformer.convert_to_graph_documents([Document(page_content=chunk)])

        add_relation_embeddings(graph_documents)

        graph.add_graph_documents(graph_documents)

        for doc in graph_documents:
            for node in doc.nodes:
                with VectorStore() as store:
                    store.add_entity(node)

                with GraphStore(uri=os.getenv("NEO4J_HYBRID_URI"), password=os.getenv("NEO4J_HYBRID_PASSWORD")) as graph_store:
                    graph_store.link_node_with_chunk(node, chunk_id)
    
def handle_documents(request):
    document_name, document_content = request.json['documentName'], request.json['documentContent']

    chunks = split_to_chunks(document_content)

    llm = ChatOpenAI(temperature=0, model="gpt-4o")

    llm_transformer = LLMGraphTransformer(llm=llm, prompt=extraction_prompt)

    graph = Neo4jGraph(url=os.getenv("NEO4J_HYBRID_URI"), password=os.getenv("NEO4J_HYBRID_PASSWORD"))

    for chunk in chunks:
        if chunk == '':
            continue

        add_chunk_to_db(graph, llm_transformer, chunk)

    return jsonify({"resultMessage": f"document {document_name} added"})