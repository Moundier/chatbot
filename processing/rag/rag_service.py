import requests

from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import WhatsAppChatLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import TextLoader

from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores import PGVector

from langchain.text_splitter import CharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_core.vectorstores import VectorStoreRetriever

import ollama
import aiohttp
import json
import sys

OLLAMA_MODEL = "llama3.2"

def ollama_query_response(question: str, context: str) -> str:
    
    response = ollama.chat(
        OLLAMA_MODEL,
        messages = [
            {'role': "system", "content": "Always answer in Brazillian Portguese. Use the given context to answer the question. If you don't know the answer, say you don't know. Don't make up answers. Use three sentence maximum and keep the answer concise. Context: {context}"},
            {'role': "user", "content": question}
        ]
    )

    sys.stdout.write(f'Response: {json.dumps(response, indent=2)}')

    response_content: str = response['message']['content']

    return response_content

def vectorizer_to_pgvector(docs_splits: list, collection_name: str = "rag-chroma") -> Chroma:
    """
    Converts documents to embeddings and stores them in a PGVector (Chroma) database asynchronously.
    """
    embedding_model = OllamaEmbeddings(model="nomic-embed-text", base_url="http://localhost:11434")
    
    chroma = Chroma.from_documents(
        documents=docs_splits,
        collection_name=collection_name,
        embedding=embedding_model,
    )
    
    return chroma

def retriever_from_pgvector(chroma: Chroma, k: int = 5) -> VectorStoreRetriever:
    """
    Creates a retriever from the PGVector store (Chroma) for retrieving relevant documents asynchronously.
    """
    retriever = chroma.as_retriever(search_kwargs={'k': k})
    return retriever

def load_and_split_data(urls: list) -> list:
    """
    Load and split documents from the provided URLs asynchronously.
    """
    docs = []
    for url in urls:
        loader = WebBaseLoader(url)
        loaded_docs = loader.load()
        docs.extend(loaded_docs)
    
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=7500, chunk_overlap=100)
    docs_splits = text_splitter.split_documents(documents=docs)
    
    return docs_splits

async def split_text_from_file(file_content: str) -> list:
    """
    Splits the text content from the file into smaller chunks asynchronously.
    """
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=7500, chunk_overlap=100)
    docs_splits = text_splitter.split_documents(documents=[{"page_content": file_content}])
    return docs_splits
