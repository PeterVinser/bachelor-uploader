from flask import jsonify
import app.services.vector.delete_documents as vector
import app.services.graph.delete_documents as graph
import app.services.hybrid.delete_documents as hybrid

def handle_delete_document(type, request):
    match(type):
        case 'vector':
            return vector.handle_delete_document(request)
        case 'graph':
            return graph.handle_delete_documents(request)
        case 'hybrid':
            return hybrid.handle_delete_documents(request)
        
    return jsonify({"error": "internal error"}), 400