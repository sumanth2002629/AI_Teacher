from langchain.chains import RetrievalQA
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.manager import CallbackManager
from langchain_community.llms import Ollama
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
import streamlit as st
import os
import time
import backend.asr as asr
import backend.text_to_pdf as text_to_pdf


# first: pip install pysqlite3-binary
# then in settings.py:

# these three lines swap the stdlib sqlite3 lib with the pysqlite3 package
# __import__('pysqlite3')
# import sys
# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')


if not os.path.exists('files'):
    os.mkdir('files')

if not os.path.exists('jj'):
    os.mkdir('jj')

if 'template' not in st.session_state:
    st.session_state.template = """You are a knowledgeable chatbot, here to help with questions of the user. Your tone should be professional and informative.

    Context: {context}
    History: {history}

    User: {question}
    Chatbot:"""
if 'prompt' not in st.session_state:
    st.session_state.prompt = PromptTemplate(
        input_variables=["history", "context", "question"],
        template=st.session_state.template,
    )
if 'memory' not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(
        memory_key="history",
        return_messages=True,
        input_key="question")
if 'vectorstore' not in st.session_state:
    st.session_state.vectorstore = Chroma(persist_directory='jj',
                                          embedding_function=OllamaEmbeddings(base_url='http://localhost:11434',
                                                                              model="llama3")
                                          )
if 'llm' not in st.session_state:
    st.session_state.llm = Ollama(base_url="http://localhost:11434",
                                  model="llama3",
                                  verbose=True,
                                  callback_manager=CallbackManager(
                                      [StreamingStdOutCallbackHandler()]),
                                  )

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

st.title("PDF Chatbot")

# Upload a PDF file
uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav"])

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["message"])

pdf_name = "transcript.pdf"
if uploaded_file is not None:
    text = asr.aud_to_text(uploaded_file.name)

    
    with st.status("Analyzing your document..."):

        asr.whispertxt_to_pdf(text,"files/transcript.pdf")


        # bytes_data = uploaded_file.read()
        # f = open("files/"+uploaded_file.name, "wb")
        # f.write(bytes_data)
        # f.close()
        loader = PyPDFLoader("files/"+pdf_name)
        data = loader.load()
        # Initialize text splitter

        
        # text_splitter = RecursiveCharacterTextSplitter(
        #     chunk_size=5000,
        #     chunk_overlap=200,
        #     length_function=len
        # )
        # all_splits = text_splitter.split_documents(data)
        f=open("new.txt","w")
        f.write(str(data))
        f.close()
        # if data:
        #     st.write("Data read successfully")
        # else:
        #     st.write("Datat not read")
        # Create and persist the vector store
        st.session_state.vectorstore = Chroma.from_documents(
            documents=data,
            embedding=OllamaEmbeddings(model="llama3")
        )
        st.session_state.vectorstore.persist()
    # st.write(len(all_splits), len(data))
    st.session_state.retriever = st.session_state.vectorstore.as_retriever()
    # Initialize the QA chain
    if 'qa_chain' not in st.session_state:
        st.session_state.qa_chain = RetrievalQA.from_chain_type(
            llm=st.session_state.llm,
            chain_type='stuff',
            retriever=st.session_state.retriever,
            verbose=True,
            chain_type_kwargs={
                "verbose": True,
                "prompt": st.session_state.prompt,
                "memory": st.session_state.memory,
            }
        )

    # Chat input
    if user_input := st.chat_input("You:", key="user_input"):
        print(user_input)
        print(type(user_input))
        user_message = {"role": "user", "message": user_input}
        st.session_state.chat_history.append(user_message)
        with st.chat_message("user"):
            st.markdown(user_input)
        with st.chat_message("assistant"):
            with st.spinner("Assistant is typing..."):
                response = st.session_state.qa_chain(user_input)
            message_placeholder = st.empty()
            full_response = ""
            sentences = []
            for chunk in response['result'].split():
                full_response += chunk + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            
            sentences.append(full_response)

            message_placeholder.markdown(full_response)

        chatbot_message = {"role": "assistant", "message": response['result']}
        st.session_state.chat_history.append(chatbot_message)
        
        text_to_pdf.write_list_to_pdf("notes.pdf", sentences)

else:
    st.write("Please upload an audio file.")





# You are an excellent teacher. The document given to you is a transcribed notes pdf of a lecture. Your job is to generate good structured notes from a pdf. The final output should be a structured notes pdf, these notes should have everything from the document given to you. These notes should be structured in such a way that the student can understand the topics easily. The document given to you has timestamps for each sentence as start and end. Your final output notes should have topicwise timestamps given as reference.