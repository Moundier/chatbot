from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.text_splitter import CharacterTextSplitter

from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever
from typing import List

# Initialize Chat Model
model_local = ChatOllama(model="mistral")

# 1. Load and split data into chunks
urls: list = [
    "https://ollama.com",
    "https://ollama.com/blog/windows-preview",
    "https://ollama.com/blog/openai-compatibility",
]

docs: list = []
for url in urls:
    loader = WebBaseLoader(url)
    loaded_docs = loader.load()
    docs.extend(loaded_docs)  # Append all documents from each URL

# Check document load status
print("Loaded documents:", len(docs))

# Split documents
text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=7500, chunk_overlap=100)
docs_splits = text_splitter.split_documents(documents=docs)

# Convert documents to Embeddings and store them in the vector database
embedding_model = OllamaEmbeddings(model="nomic-embed-text")
chroma = Chroma.from_documents(
    documents=docs_splits,
    collection_name="rag-chroma",
    embedding=embedding_model,
    # chroma server
    client_settings={
        # "chroma_api_impl": "rest",
        "chroma_server_host": "localhost",
        "chroma_server_http_port": 8000
    }
)

retriever = chroma.as_retriever(search_kwargs={'k': len(docs),})

# 3. Before RAG
println("\nBefore RAG")
before_rag_template = "What is {topic}"
before_rag_prompt = ChatPromptTemplate.from_template(before_rag_template)
before_rag_chain = before_rag_prompt | model_local | StrOutputParser()
println(before_rag_chain.invoke({"topic": "Ollama"}))

# 4. After RAG
println("\nAfter RAG")
after_rag_template = """Answer the question based only on the following context:
{context}
Question: {question}
"""
after_rag_prompt = ChatPromptTemplate.from_template(after_rag_template)
after_rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | after_rag_prompt 
    | model_local 
    | StrOutputParser()
)

println(after_rag_chain.invoke("What is Ollama?"))

def println(string: str) -> None:
    print("\n" + string)