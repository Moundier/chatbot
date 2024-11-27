import requests
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_core.vectorstores import VectorStoreRetriever

import aiohttp
import json

OLLAMA_API_URL = "http://localhost:11434/v1/chat/completions"
# OLLAMA_API_URL = "http://localhost:11434/api/generate"

async def ollama_query_response(question: str, context: str) -> str:
    """
    Queries the Ollama model via HTTP asynchronously.
    """
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "mistral",
        "messages": [
            {
                "role": "system",
                "content": f"Use the given context to answer the question. If you don't know the answer, say you don't know. "
                           f"Don't make up answers. Use three sentences maximum and keep the answer concise. Context: {context}",
            },
            {"role": "user", "content": question},
        ],
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(OLLAMA_API_URL, json=payload, headers=headers) as response:
            if response.status != 200:
                return f"Error: Status {response.status} from Ollama"

            result = await response.json()

            # {
            #     'id': 'chatcmpl-633',
            #     'object': 'chat.completion',
            #     'created': 1732699888,
            #     'model': 'mistral',
            #     'system_fingerprint': 'fp_ollama',
            #     'choices': [
            #         {
            #             'index': 0,
            #             'message': {
            #                 'role': 'assistant',
            #                 'content': " Sim, eu posso falar português. Posso ajudá-lo?\n\n*Escolha uma opção: \\n1. Como se dizer em Inglês “I don't know the answer”? 2. Qual é o nome completo do presidente da França?*\n\nExibir respostas:\n\n\\n1. I don't know the answer – Não conheço a resposta\n2. The full name of the President of France is Emmanuel Macron. – O nome completo do Presidente da França é Emmanuel Macron."
            #             },
            #             'finish_reason': 'stop'
            #         }
            #     ],
            #     'usage': {
            #         'prompt_tokens': 16,
            #         'completion_tokens': 137,
            #         'total_tokens': 153
            #     }
            # }

            content = result['choices'][0]['message']['content']

            return result
            # return result.get("text", "Sorry, I don't know the answer.")

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

async def main():
    urls = [
        "https://ollama.com",
        "https://ollama.com/blog/windows-preview",
        "https://ollama.com/blog/openai-compatibility",
    ]

    docs_splits = await load_and_split_data(urls)
    chroma = await vectorizer_to_pgvector(docs_splits)

    query = "What is Ollama?"
    retriever = await retriever_from_pgvector(chroma)
    context_documents = retriever.get_relevant_documents(query)
    context = "\n".join([doc.page_content for doc in context_documents])

    answer = await ollama_query_response(query, context)

    qa_dict = {'question': query, 'answer': answer}
    qa_json = json.dumps(qa_dict, indent=1)

    print(qa_json)

# if __name__ == "__main__":
#     main()
