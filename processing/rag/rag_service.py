from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import WhatsAppChatLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import TextLoader

from langchain_community.vectorstores import Chroma
from langchain_postgres import PGVector
from langchain_postgres.vectorstores import PGVector

from langchain_ollama import OllamaEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_core.vectorstores import VectorStoreRetriever

from typing import List
from langchain_core.documents import Document

import requests
import aiohttp
import ollama
import json
import sys

# docker exect -it ollama /bin/bash
# ollama pull llama3.2; ollama pull nomic-embed-text 

OLLAMA_MODEL = "llama3.2"

def ollama_query_response(question: str, context: str) -> str:
    try:
        context = context or "No additional context."
        
        response = ollama.chat(
            OLLAMA_MODEL,
            messages = [
                {'role': "system", "content": f"Always answer in Brazillian Portuguese. Use the given context to answer the question. If you don't know the answer, say you don't know. Don't make up answers. Use one sentence maximum and keep the answer concise. Context: {context}"},
                {'role': "user", "content": question}
            ]
        )

        response_content: str = response["message"]["content"]
        sys.stdout.write(f'\nResponse: {response_content}\n')

        return response_content
    except Exception as e:
        sys.stderr.write(f"Error in ollama_query_response: {e}\n")
        return "An error occurred."

def vectorizer_to_chroma(docs_splits: list, collection_name: str = "rag-chroma") -> Chroma:
    try:
        embedding_model = OllamaEmbeddings(model="nomic-embed-text", base_url="http://localhost:11434")
        
        chroma = Chroma.from_documents(
            documents=docs_splits,
            collection_name=collection_name,
            embedding=embedding_model,
        )
        
        return chroma
    except Exception as e:
        sys.stderr.write(f"Error in vectorizer_to_chroma: {e}\n")
        return None

def retrieve_from_pgvector(query: str) -> List:
    try:
        CONNECTION = "postgresql+psycopg://postgres:postgres@localhost:5432/vector_db"
        COLLECTION_NAME = "my_docs"

        embedding_model = OllamaEmbeddings(model="nomic-embed-text", base_url="http://localhost:11434")

        vector_store = PGVector(
            embeddings=embedding_model,
            collection_name=COLLECTION_NAME,
            connection=CONNECTION,
            use_jsonb=True,
        )

        query_embedding: List[float] = embedding_model.embed_query(query)
        sys.stdout.write(f"\nEmbedding: {query_embedding}\n")

        results = vector_store.similarity_search_by_vector(query_embedding, k=3)

        for doc in results:
            sys.stdout.write(f"* Doc {doc.page_content} [{doc.metadata}]")

        sys.stdout.write(f"\nResults: {results}\n")
        return results

    except Exception as e:
        sys.stderr.write(f"Error in retrieve_from_pgvector: {e}\n")
        return []

def retriever_from_chroma(chroma: Chroma, k: int = 5) -> VectorStoreRetriever:
    try:
        retriever = chroma.as_retriever(search_kwargs={'k': k})
        return retriever
    except Exception as e:
        sys.stderr.write(f"Error in retriever_from_chroma: {e}\n")
        return None

def load_and_split_data(urls: list) -> list:
    try:
        docs = []
        for url in urls:
            loader = WebBaseLoader(url)
            loaded_docs = loader.load()
            docs.extend(loaded_docs)
        
        text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=7500, chunk_overlap=100)
        docs_splits = text_splitter.split_documents(documents=docs)
        
        sys.stdout.write(f"Documents\n {docs}")
        return docs_splits
    except Exception as e:
        sys.stderr.write(f"Error in load_and_split_data: {e}\n")
        return []

async def split_text_from_file(file_content: str) -> list:
    try:
        text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=7500, chunk_overlap=100)
        docs_splits = text_splitter.split_documents(documents=[{"page_content": file_content}])
        return docs_splits
    except Exception as e:
        sys.stderr.write(f"Error in split_text_from_file: {e}\n")
        return []