import asyncio
import json
import time
from langchain_core.vectorstores import VectorStoreRetriever
from aio_pika import connect_robust, Message, IncomingMessage
from rag.rag_service import ollama_query_response
from rag.rag_service import retriever_from_pgvector
from rag.rag_service import load_and_split_data
from rag.rag_service import vectorizer_to_pgvector

from rabbit.rabbit_config import AMQP_CONNECTION_URL, INPUT_QUEUE, OUTPUT_QUEUE

async def process_message(message: IncomingMessage) -> None:
    """
    Process a single message from the RabbitMQ queue.
    """
    async with message.process():
        try:
            data = json.loads(message.body.decode())

            question: str = data.get("content", "").strip()

            print(question)
            
            if not question:
                raise ValueError("Missing 'content' (question) in the message.")

            print(f"Incoming Message: {question}")

            # STARTS VECTORIZER
            # Load and process documents
            urls = [
                "https://ollama.com",
                "https://ollama.com/blog/windows-preview",
                "https://ollama.com/blog/openai-compatibility",
            ]

            docs_splits = load_and_split_data(urls)
            for doc in docs_splits:
                print(doc)
            
            # Vectorization and retrieval
            chroma = vectorizer_to_pgvector(docs_splits)
            # ENDS VECTORIZER

            # RETRIEVER
            retriever: VectorStoreRetriever = retriever_from_pgvector(chroma)  
            
            context_documents = retriever.get_relevant_documents(query=question)
            context = "\n".join([doc.page_content for doc in context_documents])
            print(f"Context: {context}")
            response = ollama_query_response(question, context)
            print(f"Response: {response}")

            data.update({
                "response": response,
                "processed_at": time.ctime()
            })

            # Publish the processed message
            await message.channel.basic_publish(
                body=json.dumps(data).encode(),
                exchange='',
                routing_key=OUTPUT_QUEUE,
            )

            print()
            print(f"Processed and forwarded message: {json.dumps(data, indent=2)}\n")

        except Exception as e:
            print(f"Failed to process message: {e}")


async def consume_messages() -> None:
    """
    Consume messages from RabbitMQ and process them.
    """
    connection = await connect_robust(AMQP_CONNECTION_URL)

    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)

        # Declare queues
        input_queue = await channel.declare_queue(INPUT_QUEUE, durable=True)
        await channel.declare_queue(OUTPUT_QUEUE, durable=True)

        print(f"Listening for messages on {INPUT_QUEUE}...\n")

        async with input_queue.iterator() as queue_iter:
            async for message in queue_iter:
                await process_message(message)


