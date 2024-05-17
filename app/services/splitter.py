from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

def split_to_chunks(document_content):
    text_splitter = SemanticChunker(OpenAIEmbeddings())
    
    chunks = text_splitter.create_documents([document_content])

    return [chunk.page_content for chunk in chunks]
