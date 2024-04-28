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
import os
import time
import asr 
import text_to_pdf


def process(user_input):
    session_template = """You are a knowledgeable chatbot, here to help with questions of the user. Your tone should be professional and informative.

    Context: {context}
    History: {history}

    User: {question}
    Chatbot:"""

    prompt = ""
    memory = ""
    vectorstore = ""
    llm = ""
    chat_history = ""
    
    if(prompt==""):
        prompt =  PromptTemplate(
            input_variables=["history", "context", "question"],
            template=session_template,
        )

    if(memory==""):
        memory = ConversationBufferMemory(
                memory_key="history",
                return_messages=True,
                input_key="question")
    
    if(vectorstore==""):
        vectorstore = Chroma(persist_directory='jj',
                                            embedding_function=OllamaEmbeddings(base_url='http://localhost:11434',
                                                                                model="llama3"))
    
    if(llm==""):
        llm = Ollama(base_url="http://localhost:11434",
                                    model="llama3",
                                    verbose=True,
                                    callback_manager=CallbackManager(
                                        [StreamingStdOutCallbackHandler()]),
                                  )
    
    if(chat_history==""):
        chat_history = []

    text = asr.aud_to_text("audio.wav")
    asr.whispertxt_to_pdf(text,"transcript.pdf")


    loader = PyPDFLoader("transcript.pdf")
    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200,
        length_function=len
    )
    all_splits = text_splitter.split_documents(data)

    vectorstore = Chroma.from_documents(
            documents=all_splits,
            embedding=OllamaEmbeddings(model="llama3")
        )
    
    vectorstore.persist()

    retriever = vectorstore.as_retriever()

    qa_chain = ""

    if qa_chain=="":
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type='stuff',
            retriever=retriever,
            verbose=True,
            chain_type_kwargs={
                "verbose": True,
                "prompt": prompt,
                "memory": memory,
            }
        )

    # chat_history.append(user_input)

    response = qa_chain(user_input)

    full_response = ""
    complete_response = ""
    sentences = []
    for chunk in response['result'].split():
        full_response += chunk + " "
        time.sleep(0.05)
        # Add a blinking cursor to simulate typing    
    sentences.append(full_response)

    complete_response += full_response
    chatbot_message = {"role": "assistant", "message": response['result']}
    # chat_history.append(chatbot_message)

    text_to_pdf.write_list_to_pdf("notes.pdf", sentences)

    return complete_response

if __name__=="__main__":
    process("Please summarize the document")




