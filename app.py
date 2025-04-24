import streamlit as st
import os
import random
from data_loader import load_documents_from_directory
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

# Load documents if not already done
if "documents" not in st.session_state:
    with st.spinner("Setting up the knowledge base... This might take a minute."):
        documents = load_documents_from_directory("insurance_data")
        st.session_state.documents = documents
        
        # Create a dictionary to store policy information by type
        policy_info = {}
        for doc in documents:
            content = doc.page_content
            if "Health Insurance" in content:
                policy_type = "health"
            elif "Life Insurance" in content:
                policy_type = "life"
            elif "Auto Insurance" in content:
                policy_type = "auto"
            elif "Home Insurance" in content:
                policy_type = "home"
            else:
                policy_type = "general"
                
            if policy_type not in policy_info:
                policy_info[policy_type] = []
            policy_info[policy_type].append(content)
        
        st.session_state.policy_info = policy_info

# Simple function to match keywords and provide responses
def get_insurance_response(query):
    query = query.lower()
    policy_info = st.session_state.policy_info
    
    # Handle requests for human agent
    if "human agent" in query or "speak to a person" in query or "talk to someone" in query:
        return """
        I understand you'd like to speak with a human agent. Please call our 
        customer service at 1-800-INS-HELP or email support@insurancecompany.com. 
        An agent will assist you with your specific concerns.
        """
    
    # Match based on insurance type keywords
    if any(keyword in query for keyword in ["health", "medical", "doctor", "hospital"]):
        policy_type = "health"
    elif any(keyword in query for keyword in ["life", "death", "beneficiary", "term"]):
        policy_type = "life"
    elif any(keyword in query for keyword in ["auto", "car", "vehicle", "accident", "collision"]):
        policy_type = "auto"
    elif any(keyword in query for keyword in ["home", "house", "property", "dwelling"]):
        policy_type = "home"
    else:
        policy_type = "general"
    
    # Match based on specific topics
    if "premium" in query or "cost" in query or "price" in query:
        topic = "premium"
    elif "coverage" in query or "cover" in query or "protect" in query:
        topic = "coverage"
    elif "claim" in query or "file" in query or "process" in query:
        topic = "claim"
    elif "deductible" in query:
        topic = "deductible"
    else:
        topic = "general"
    
    # Generate a response based on the matched insurance type and topic
    if policy_type != "general":
        contents = policy_info.get(policy_type, [])
        if contents:
            relevant_info = ""
            for content in contents:
                if topic == "premium" and "Premium" in content:
                    relevant_sections = [line for line in content.split('\n') if "Premium" in line or "cost" in line.lower()]
                    if relevant_sections:
                        relevant_info += "\n".join(relevant_sections) + "\n"
                elif topic == "coverage" and "Coverage" in content:
                    relevant_sections = [line for line in content.split('\n') if "Coverage" in line or "cover" in line.lower()]
                    if relevant_sections:
                        relevant_info += "\n".join(relevant_sections) + "\n"
                elif topic == "claim" and "Claims Process" in content:
                    start_idx = content.find("Claims Process")
                    end_idx = content.find("##", start_idx + 1)
                    if end_idx == -1:
                        end_idx = len(content)
                    relevant_info += content[start_idx:end_idx] + "\n"
                elif topic == "deductible" and "Deductible" in content:
                    relevant_sections = [line for line in content.split('\n') if "Deductible" in line]
                    if relevant_sections:
                        relevant_info += "\n".join(relevant_sections) + "\n"
            
            if relevant_info:
                return f"Based on our information about {policy_type} insurance:\n\n{relevant_info}\n\nIs there anything specific about this you'd like to know more about?"
    
    # If no specific match was found, provide a general response
    insurance_types = {
        "health": "Health insurance covers medical expenses such as doctor visits, hospital stays, and prescription medications.",
        "life": "Life insurance provides financial protection to your beneficiaries in the event of your death.",
        "auto": "Auto insurance protects you against financial loss in the event of a vehicle accident or theft.",
        "home": "Home insurance covers damage to your home and belongings, as well as liability for injuries that occur on your property."
    }
    
    if policy_type in insurance_types:
        return f"{insurance_types[policy_type]}\n\nWhat specific information would you like about {policy_type} insurance?"
    else:
        return """
        We offer several types of insurance policies including health, life, auto, and home insurance.
        Each policy has different coverage options, premiums, and claim processes.
        
        Could you please specify which type of insurance you're interested in learning more about?
        """

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
        
        with st.spinner("Thinking..."):
            # Get response
            response = get_insurance_response(prompt)
        
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
