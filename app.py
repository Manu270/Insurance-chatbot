import streamlit as st
import os
from data_loader import load_documents_from_directory
from database import get_vectorstore
from llm_handler import get_qa_chain, get_openai_llm
from utils import initialize_session_state, get_chat_history

# Set page configuration
st.set_page_config(
    page_title="Insurance Policy Chatbot",
    page_icon="💬",
    layout="wide"
)

# Initialize session state for chat history and more
initialize_session_state()

# Page header
st.title("Insurance Policy Information Chatbot")
st.markdown("""
This AI-powered chatbot can help answer your questions about our insurance policies, 
coverage options, premiums, and claim processes. Feel free to ask any questions!
""")

# Sidebar for additional options
with st.sidebar:
    st.header("About")
    st.markdown("""
    This chatbot is designed to provide information on:
    - Health Insurance
    - Life Insurance
    - Auto Insurance
    - Home Insurance
    
    For complex queries or to speak with a human agent, please indicate in your message.
    """)
    
    # Clear conversation button
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.rerun()

# Main chat interface
st.subheader("Chat")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Load documents and create vector store if not already done
if "vectorstore" not in st.session_state:
    with st.spinner("Setting up the knowledge base... This might take a minute."):
        documents = load_documents_from_directory("insurance_data")
        vectorstore = get_vectorstore(documents)
        st.session_state.vectorstore = vectorstore

# Initialize the QA chain if not already done
if "qa_chain" not in st.session_state:
    with st.spinner("Initializing the AI model..."):
        llm = get_openai_llm()
        qa_chain = get_qa_chain(st.session_state.vectorstore, llm)
        st.session_state.qa_chain = qa_chain

# Chat input
if prompt := st.chat_input("Ask about our insurance policies..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Get chat history for context
        chat_history = get_chat_history(st.session_state.chat_history)
        
        # Process with fallback for complex queries
        if "human agent" in prompt.lower() or "speak to a person" in prompt.lower():
            response = """
            I understand you'd like to speak with a human agent. Please call our 
            customer service at 1-800-INS-HELP or email support@insurancecompany.com. 
            An agent will assist you with your specific concerns.
            """
        else:
            try:
                with st.spinner("Thinking..."):
                    # Get response from QA chain
                    response = st.session_state.qa_chain(
                        {"question": prompt, "chat_history": chat_history}
                    )
                    
                    # Check if we need to escalate to a human
                    if "I don't know" in response["answer"] or "I'm not sure" in response["answer"]:
                        response["answer"] += "\n\nThis seems to be a complex query. Would you like me to connect you with a human agent for more detailed assistance?"
                    
                    response = response["answer"]
            except Exception as e:
                response = f"""
                I apologize, but I'm having trouble processing your request at the moment. 
                This might be a complex query that would be better addressed by one of our 
                human insurance specialists. Please call our customer service at 1-800-INS-HELP 
                or try rephrasing your question.
                
                Technical details (for support): {str(e)}
                """
        
        # Display the response
        message_placeholder.write(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Update chat history for context
    st.session_state.chat_history.append((prompt, response))

# Add a footer
st.markdown("""
---
*Note: This chatbot provides general information about insurance policies. 
For personalized advice or to purchase a policy, please contact our customer service.*
""")
