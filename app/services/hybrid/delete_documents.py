from flask import jsonify

def handle_delete_documents(request):
    document_name = request.json['documentName']

    return jsonify({"resultMessage": f"document {document_name} deleted"})