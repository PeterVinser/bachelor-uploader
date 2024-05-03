from flask import jsonify
import app.services.graph.add_documents as graph
import app.services.hybrid.add_documents as hybrid
import app.services.vector.add_documents as vector

def handle_add_document(type, request):
    match(type):
        case 'vector':
            return vector.handle_add_documents(request)
        case 'graph':
            return graph.handle_documents(request)
        case 'hybrid':
            return hybrid.handle_documents(request)
        
    return jsonify({"error": "internal error"}), 400