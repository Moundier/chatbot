import pika
import time
import json
import sys

rabbitmq_config = {
    host: '0.0.0.0',
    enqueue: {
        wpp: 'WPP_QUEUE'
    },
    consume: {
        sync: 'SYNC_QUEUE'
    },
}

# RabbitMQ connection settings
RABBITMQ_HOST = 'localhost'
INPUT_QUEUE = 'input_queue'
OUTPUT_QUEUE = 'output_queue'

def create_connection():
    try:
        return pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    except pika.exceptions.AMQPConnectionError as e:
        sys.stderr.write(f"Error connecting to RabbitMQ: {e}\n")
        sys.exit(1)

def process_message(body):
    try:
        payload = json.loads(body.decode()) 
        sys.stdout.write(f"Processing message: {payload}\n")

        payload['processed'] = True
        payload['processed_at'] = time.ctime()

        return payload
    except Exception as e:
        sys.stderr.write(f"Error processing message: {e}\n")
        sys.exit(1)

def enqueue(message, queue_name):
    try:
        connection = create_connection()
        channel = connection.channel()
        channel.queue_declare(queue=queue_name, durable=True)

        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2)  
        )

        sys.stdout.write(f"Sent message to {queue_name}: {message}\n")
        connection.close()
    except Exception as e:
        sys.stderr.write(f"Error sending message to {queue_name}: {e}\n")
        sys.exit(1)

def callback(ch, method, properties, body):
    try:
        processed_message = process_message(body)

        send_message(processed_message, OUTPUT_QUEUE)

        ch.basic_ack(delivery_tag=method.delivery_tag)
        sys.stdout.write(f"Message processed and sent to {OUTPUT_QUEUE}\n")
    except Exception as e:
        sys.stderr.write(f"Error in callback: {e}\n")
        sys.exit(1)

def consume_messages():
    try:
        connection = create_connection()
        channel = connection.channel()

        channel.queue_declare(queue=INPUT_QUEUE, durable=True)
        channel.basic_qos(prefetch_count=1)  

        channel.basic_consume(queue=INPUT_QUEUE, on_message_callback=callback)

        sys.stdout.write(f"Listening for messages on {INPUT_QUEUE}...\n")
        channel.start_consuming()
    except Exception as e:
        sys.stderr.write(f"Error consuming messages: {e}\n")
        sys.exit(1)

if __name__ == '__main__':
    try:
        consume_messages()
    except KeyboardInterrupt:
        sys.stderr.write("Shutting down...\n")
        sys.exit(0)
