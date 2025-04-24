import os
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI

def get_openai_llm(temperature=0):
    """
    Get the OpenAI language model.
    
    Args:
        temperature (float): Temperature parameter for controlling randomness.
    
    Returns:
        ChatOpenAI: The language model.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    # The newest OpenAI model is "gpt-4o" which was released May 13, 2024.
    # do not change this unless explicitly requested by the user
    return ChatOpenAI(
        openai_api_key=api_key,
        model="gpt-4o",
        temperature=temperature
    )

def get_qa_chain(vectorstore, llm):
    """
    Create a conversational QA chain using the vector store and language model.
    
    Args:
        vectorstore: Vector store for retrieving relevant documents.
        llm: Language model for generating responses.
    
    Returns:
        ConversationalRetrievalChain: The QA chain.
    """
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )
    
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=False,
        verbose=True
    )
    
    return chain

def get_system_prompt():
    """
    Get the system prompt for the language model.
    
    Returns:
        str: System prompt.
    """
    return """
    You are an insurance policy information assistant. Your role is to help customers 
    understand different insurance policies, coverage options, premiums, claims processes, 
    and other insurance-related information.
    
    Provide accurate, helpful, and concise responses based on the information available 
    in the knowledge base. If you're unsure about something or if a question is outside 
    the scope of insurance policies, acknowledge your limitations and suggest the customer 
    speak with a human agent.
    
    For complex or highly specific questions about individual policies, suggest that the 
    customer contact a human agent for personalized assistance.
    
    Be professional, empathetic, and focused on helping the customer understand their 
    insurance options.
    """
