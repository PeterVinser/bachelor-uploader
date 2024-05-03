from flask import jsonify
from neo4j import GraphDatabase
import os

def handle_delete_documents(request):
    document_name = request.json['documentName']

    driver = GraphDatabase.driver(uri=os.getenv("NEO4J_URI"), auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD")))

    with driver.session() as session:
        query = """
        MATCH(n {DocumentName: $name})
        DETACH DELETE n
        """

        session.run(query, name=document_name)

    driver.close()

    return jsonify({"resultMessage": f"document {document_name} deleted"})