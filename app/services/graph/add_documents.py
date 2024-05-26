from flask import jsonify
from langchain_community.graphs.neo4j_graph import Neo4jGraph
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from app.services.splitter import split_to_chunks
import os
from app.services.graph_store import extraction_prompt

def handle_documents(request):
    document_name, document_content = request.json['documentName'], request.json['documentContent']

    chunks = split_to_chunks(document_content)

    graph = Neo4jGraph(url=os.getenv("NEO4J_GRAPH_URI"), password=os.getenv("NEO4J_GRAPH_PASSWORD"))

    llm = ChatOpenAI(temperature=0, model="gpt-4o")

    llm_transformer = LLMGraphTransformer(llm=llm, prompt=extraction_prompt)

    documents = [Document(page_content=chunk) for chunk in chunks]

    graph_documents = llm_transformer.convert_to_graph_documents(documents)

    graph.add_graph_documents(graph_documents)

    return jsonify({"resultMessage": f"document {document_name} added"})