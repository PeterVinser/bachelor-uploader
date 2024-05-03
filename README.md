# bachelor-uploader

This is an uploader API for bachelor's thesis app that serves as an admin for RAG service.

The API has three main methods and each has three endpoints:
- /api/add/
    - /api/add/vector/
    - /api/add/graph/
    - /api/add/hybrid/
- /api/update/
    - /api/update/vector/
    - /api/update/hybrid/
    - /api/update/graph/
- /api/delete/
    - /api/delete/vector/
    - /api/delete/graph/
    - /api/delete/hybrid/

Each type of method (vector, graph, hybrid) accepts the same requests, only saves to a different type of RAG service.

## Add

Adds a given document for all retrieval types (vector-db, graph and fusion based)

### Request:

Body:

{
    "documentName": <document name>,
    "documentContent": <document content>
}

### Response

Body:

{
    "resultMessage": <result of addition>
}

## Update

This is a placeholder. This component may not be used in the end.

## Delete

Deletes all documents with specified name.

### Request:

Body:

{
    "documentName": <document name>
}

### Response

Body:

{
    "resultMessage": <result of deletion>
}