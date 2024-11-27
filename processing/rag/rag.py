from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables import Runnable
from langchain_core.runnables import RunnableBinding
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.text_splitter import CharacterTextSplitter

from langchain_ollama import ChatOllama, OllamaEmbeddings

from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever
from typing import List, Dict, Any

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

import json

def query_ollama(question: str, context: str) -> str:
    headers = {
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": "mistral",
        "messages": [
            {"role": "system", "content": "Use the given context to answer the question. If you don't know the answer, say you don't know. Don't make up answers. Use three sentence maximum and keep the answer concise. Context: {context}"},
            {"role": "user", "content": question}
        ],
        "stream": True,
    }
    
    response = requests.post(OLLAMA_API_URL, json=payload, headers=headers, stream=True)

    if response.status_code != 200:
        sys.stderr.write(f"Error: {response.status_code}\n\n")
        sys.exit(1)

    response_data = response.json()
    
    answer = response_data.get("text", "Sorry, I don't know the answer.")

    # answer = query_ollama(query, context)
    
    return answer

llm = ChatOllama(model="mistral", base_url="http://localhost:11434")

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

# Split documents
text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=7500, chunk_overlap=100)
docs_splits = text_splitter.split_documents(documents=docs)

# Convert documents to Embeddings and store them in the vector database
embedding_model = OllamaEmbeddings(model="nomic-embed-text")
chroma = Chroma.from_documents(
    documents=docs_splits,
    collection_name="rag-chroma",
    embedding=embedding_model,
)

print("Document lenght: " + str(len(docs)))
retriever = chroma.as_retriever(search_kwargs={'k': len(docs)})

query: str = "What is Ollama?"

# 1. LangChain
# system_prompt: str = (
#     "Use the given context to answer the question. "
#     "If you don't know the answer, say you don't know. Don't make up answers."
#     "Use three sentence maximum and keep the answer concise. "
#     "Context: {context}"
# )

# prompt: ChatPromptTemplate = ChatPromptTemplate.from_messages(
#     [
#         ("system", system_prompt),
#         ("human", "{input}"),
#     ]
# )

# question_answer_chain: RunnableBinding = create_stuff_documents_chain(llm, prompt)
# chain: RunnableBinding = create_retrieval_chain(retriever, question_answer_chain)
# response: dict = chain.invoke({"input": query}) 
# answer: str = response.get('answer')

# qa_dict = {
#     'question': query,
#     'answer': answer
# }

# qa_json = json.dumps(qa_dict, indent=1)

# print(qa_json)

# 2. Optimized 
context_documents = retriever.get_relevant_documents(query)
context = "\n".join([doc.page_content for doc in context_documents])

# Generate the answer using Ollama model via the HTTP request
answer = query_ollama(query, context)

qa_dict = {
    'question': query,
    'answer': answer
}

qa_json = json.dumps(qa_dict, indent=1)

print(qa_json)