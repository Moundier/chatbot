import traceback
import asyncio
import json
import time
import sys

from langchain_core.vectorstores import VectorStoreRetriever
from aio_pika import connect_robust, Message, IncomingMessage
from rag.rag_service import ollama_query_response
from rag.rag_service import retriever_from_chroma
from rag.rag_service import load_and_split_data
from rag.rag_service import vectorizer_to_chroma

from rag.rag_service import retrieve_from_pgvector

from typing import Any

from rabbit.rabbit_config import AMQP_CONNECTION_URL, INPUT_QUEUE, OUTPUT_QUEUE

async def process_message(message: IncomingMessage) -> None:
    """
    Process a single message from the RabbitMQ queue.
    """
    async with message.process():
        try:
            data = json.loads(message.body.decode())
            question = data.get("content")

            if not question:
                raise ValueError("Missing 'content' in the message.")

            sys.stdout.write(f"\nIncoming Message: '{question}'\n")

            context = retrieve_from_pgvector(query=question)
            response = ollama_query_response(question=question, context=context)

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
    
            sys.stdout.write(f"\nConsuming messages on processing_queue...\n")

        except Exception as e:
            sys.stdout.write(f"\nFailed to process message: {str(e)}\n")
            sys.stdout.write(f"Stack trace: {traceback.format_exc()}\n")

async def consume_messages() -> None:

    connection = await connect_robust(AMQP_CONNECTION_URL)

    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)

        input_queue = await channel.declare_queue(INPUT_QUEUE, durable=True)
        await channel.declare_queue(OUTPUT_QUEUE, durable=True)

        sys.stdout.write(f"\nConsuming messages on {INPUT_QUEUE}...\n")

        async with input_queue.iterator() as queue_iterator:
            async for message in queue_iterator:
                await process_message(message)


