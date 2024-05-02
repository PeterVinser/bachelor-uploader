# bachelor-uploader

This is an uploader API for bachelor's thesis app that serves as an admin for RAG service.

The API has three endpoints:
- /api/add/
- /api/update/
- /api/delete/

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