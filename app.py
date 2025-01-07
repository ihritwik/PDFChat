import time
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template

def get_pdf_text(pdf_docs):
    text=""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
            separator = "\n",
            chunk_size = 1000,
            chunk_overlap = 200,
            length_function = len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    # embeddings = HuggingFaceInstructEmbeddings(model_name = "hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts = text_chunks, embedding = embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI(model_name="gpt-4")
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm = llm,
        retriever = vectorstore.as_retriever(),
        memory = memory
    )
    return conversation_chain

def handle_userinput(user_question):
    # Start the timer
    start_time = time.time()
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    # Stop the timer
    end_time = time.time()
    inference_time = end_time - start_time  # Calculate the inference time

    # Display the inference time in the app
    st.write(f"Inference time: {inference_time:.2f} seconds")

    for i, message in enumerate(st.session_state.chat_history):
        if i%2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

def main():
    load_dotenv()
    st.set_page_config(page_title="Chat", page_icon = ":books:")

    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with PDFs :books:")
    user_question = st.text_input("Ask a question about your document:")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("My documents")
        pdf_docs = st.file_uploader("Upload and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                # get pdf text
                raw_text = get_pdf_text(pdf_docs)
                
                # get the text chunks
                text_chunks = get_text_chunks(raw_text)
                
                # create vector database
                vectorstore = get_vectorstore(text_chunks)
                
                # Retrieve the first vector stored in the FAISS index
                index = vectorstore.index

                # Get total number of vectors in the vector database
                total_indexes = vectorstore.index.ntotal
                #print(f"Total number of vectors in the FAISS index: {total_indexes}")

                # Loop to retrieve and print the first 5 vectors and their dimensions
                for i in range(min(5, index.ntotal)):  # index.ntotal gives the total number of vectors in the FAISS index
                    vector = index.reconstruct(i)  # Retrieve the vector by index
                    #print(f"Vector {i+1}: {vector}")
                    #print(f"Dimension of vector {i+1}: {len(vector)}\n")
                
                # Create conversation chain
                st.session_state.conversation = get_conversation_chain(vectorstore)

    # st.session_state.conversation

if __name__ == '__main__':
    main()
