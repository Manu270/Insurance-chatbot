import streamlit as st

def initialize_session_state():
    """
    Initialize session state variables if they don't exist.
    """
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant", 
                "content": "Hello! I'm your insurance policy assistant. How can I help you today?"
            }
        ]
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

def get_chat_history(chat_history, k=5):
    """
    Get the most recent k chat history entries for context.
    
    Args:
        chat_history (list): Full chat history.
        k (int): Number of most recent entries to return.
    
    Returns:
        list: Most recent chat history entries.
    """
    return chat_history[-k:] if len(chat_history) > k else chat_history

def format_docs(docs):
    """
    Format a list of documents into a string.
    
    Args:
        docs (list): List of Document objects.
    
    Returns:
        str: Formatted string of document contents.
    """
    return "\n\n".join([doc.page_content for doc in docs])
