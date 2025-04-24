import os
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

def get_embedding_model():
    """
    Get the embedding model for creating vector embeddings.
    
    Returns:
        OpenAIEmbeddings: The embedding model.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    return OpenAIEmbeddings(openai_api_key=api_key)

def get_vectorstore(documents):
    """
    Create a vector store from documents using embeddings.
    
    Args:
        documents (list): List of Document objects.
    
    Returns:
        FAISS: Vector store with embedded documents.
    """
    embeddings = get_embedding_model()
    
    # Create vectorstore with embedded documents
    vectorstore = FAISS.from_documents(documents, embeddings)
    return vectorstore

def get_relevant_documents(vectorstore, query, k=4):
    """
    Retrieve the most relevant documents for a query.
    
    Args:
        vectorstore: Vector store containing document embeddings.
        query (str): Query string.
        k (int): Number of documents to retrieve.
    
    Returns:
        list: List of relevant Document objects.
    """
    return vectorstore.similarity_search(query, k=k)
