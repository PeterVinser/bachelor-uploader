from flask import jsonify
from langchain_community.graphs.neo4j_graph import Neo4jGraph
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document

def handle_documents(request):
    document_name, document_content = request.json['documentName'], request.json['documentContent']

    graph = Neo4jGraph()

    llm = ChatOpenAI(temperature=0, model="gpt-4-turbo-preview")

    llm_transformer = LLMGraphTransformer(llm=llm)

    documents = [Document(page_content=document_content)]

    graph_documents = llm_transformer.convert_to_graph_documents(documents)

    for doc in graph_documents:
        for node in doc.nodes:
            node.properties['DocumentName'] = document_name

    graph.add_graph_documents(graph_documents)

    return jsonify({"resultMessage": f"document {document_name} added"})