import pika
import time
import json
import sys

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
    """Simulate message processing."""
    try:
        payload = json.loads(body.decode())  # Decode the message (JSON format)
        sys.stderr.write(f"Processing message: {payload}\n")

        # Simulate some processing on the payload
        payload['processed'] = True
        payload['processed_at'] = time.ctime()

        return payload
    except Exception as e:
        sys.stderr.write(f"Error processing message: {e}\n")
        sys.exit(1)

def send_message(message, queue_name):
    """Send the processed message to the output queue."""
    try:
        connection = create_connection()
        channel = connection.channel()
        channel.queue_declare(queue=queue_name, durable=True)

        # Publish the message to the specified queue
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2)  # Make message persistent
        )
        sys.stderr.write(f"Sent message to {queue_name}: {message}\n")
        connection.close()
    except Exception as e:
        sys.stderr.write(f"Error sending message to {queue_name}: {e}\n")
        sys.exit(1)

def callback(ch, method, properties, body):
    """Callback function for consuming messages."""
    try:
        # Process the incoming message
        processed_message = process_message(body)

        # Send the processed message to the output queue
        send_message(processed_message, OUTPUT_QUEUE)

        # Acknowledge the message
        ch.basic_ack(delivery_tag=method.delivery_tag)
        sys.stderr.write(f"Message processed and sent to {OUTPUT_QUEUE}\n")
    except Exception as e:
        sys.stderr.write(f"Error in callback: {e}\n")
        sys.exit(1)

def consume_messages():
    """Start consuming messages from RabbitMQ."""
    try:
        connection = create_connection()
        channel = connection.channel()

        # Declare the input queue (ensure it exists)
        channel.queue_declare(queue=INPUT_QUEUE, durable=True)
        channel.basic_qos(prefetch_count=1)  # Fair dispatch (one message at a time)

        # Start consuming messages from the input queue
        channel.basic_consume(queue=INPUT_QUEUE, on_message_callback=callback)

        sys.stderr.write(f"Listening for messages on {INPUT_QUEUE}...\n")
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
