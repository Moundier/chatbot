import pika
import json
import time
import sys

class Producer:
    def __init__(self, host='localhost', queue_name='input_queue'):
        self.host = host
        self.queue_name = queue_name

    def create_connection(self):
        """Create and return a RabbitMQ connection."""
        try:
            return pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        except pika.exceptions.AMQPConnectionError as e:
            sys.stderr.write(f"Error connecting to RabbitMQ: {e}\n")
            sys.exit(1)

    def send_message(self, message):
        """Send a message to RabbitMQ."""
        try:
            connection = self.create_connection()
            channel = connection.channel()

            # Declare the queue (ensure it exists)
            channel.queue_declare(queue=self.queue_name, durable=True)

            # Publish the message to the queue
            channel.basic_publish(
                exchange='',
                routing_key=self.queue_name,
                body=json.dumps(message),
                properties=pika.BasicProperties(delivery_mode=2)  # Make message persistent
            )
            sys.stderr.write(f"Sent message to {self.queue_name}: {message}\n")
            connection.close()
        except Exception as e:
            sys.stderr.write(f"Error sending message to {self.queue_name}: {e}\n")
            sys.exit(1)

    def generate_message(self):
        """Generate a sample message to send."""
        message = {
            'id': time.time(),  # Use current time as a unique ID
            'content': 'This is a test message for RabbitMQ.'
        }
        return message

if __name__ == '__main__':
    producer = Producer()

    # Send a new message to the queue every 5 seconds
    while True:
        try:
            message = producer.generate_message()
            producer.send_message(message)
            time.sleep(5)
        except KeyboardInterrupt:
            sys.stderr.write("Shutting down producer...\n")
            sys.exit(0)
        except Exception as e:
            sys.stderr.write(f"Unexpected error: {e}\n")
            sys.exit(1)
