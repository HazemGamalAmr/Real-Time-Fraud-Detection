import gzip
import base64
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from confluent_kafka import Consumer, KafkaError
from google.cloud import pubsub_v1
from google.api_core.retry import Retry  # Updated import for retry
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Google Pub/Sub configuration
gcp_project_id = "iti-graduation-project-434313"
pubsub_topic = "streaming_data"
gcp_credentials_file = 'iti-graduation-project-434313-14030620b9e0.json'

# Initialize the Pub/Sub Publisher Client with batch settings for performance
batch_settings = pubsub_v1.types.BatchSettings(
    max_bytes=500 * 1024,  # 500 KB max batch size
    max_latency=1,  # Send batch after 1 second
    max_messages=200  # Max 200 messages per batch
)

publisher = pubsub_v1.PublisherClient.from_service_account_json(
    gcp_credentials_file, batch_settings=batch_settings
)
topic_path = publisher.topic_path(gcp_project_id, pubsub_topic)

# Correct Kafka consumer configuration
kafka_config = {
    'bootstrap.servers': 'localhost:9092',  # Kafka broker address
    'group.id': 'my-group',
    'auto.offset.reset': 'earliest',
    'fetch.min.bytes': 1048576,  # 1 MB
    'max.partition.fetch.bytes': 52428800,  # 50 MB
    'compression.codec': 'gzip',  # Compression for Kafka messages
    'session.timeout.ms': 6000,  # Session timeout
    'request.timeout.ms': 30000,  # 30 seconds timeout
    'enable.auto.commit': True,  # Enable auto commit
    'auto.commit.interval.ms': 5000,  # Commit interval
}

kafka_topic = 'kafkaTopic_final_1'

# Initialize Kafka consumer
consumer = Consumer(kafka_config)
consumer.subscribe([kafka_topic])

# Pub/Sub Retry Configuration using google.api_core.retry.Retry
retry_policy = Retry(
    initial=0.5,  # Start with a 500 ms delay
    maximum=5.0,  # Maximum backoff of 5 seconds
    multiplier=1.5,  # Increase delay by 1.5x on each retry
    deadline=30.0  # Total timeout of 30 seconds
)

# Additional global variables to keep track of message statistics
total_messages_sent = 0
total_bytes_sent = 0

def compress_message(message):
    """Compress the message using gzip and encode with base64."""
    compressed = gzip.compress(message.encode('utf-8'))
    return base64.b64encode(compressed).decode('utf-8')

def publish_to_pubsub(message):
    """Publish a message to Google Pub/Sub with error handling."""
    global total_messages_sent, total_bytes_sent
    try:
        compressed_message = compress_message(message)
        future = publisher.publish(topic_path, compressed_message.encode('utf-8'), retry=retry_policy)
        future.result()  # Block until the message is published
        
        # Update and log message statistics
        message_size = len(compressed_message.encode('utf-8'))
        total_messages_sent += 1
        total_bytes_sent += message_size
        
        logging.info(f"Published message to Pub/Sub: {compressed_message[:50]}... (Size: {message_size} bytes)")
        logging.info(f"Total messages sent: {total_messages_sent}, Total bytes sent: {total_bytes_sent / 1024:.2f} KB")
    except Exception as e:
        logging.error(f"Error publishing to Pub/Sub: {e}")

def consume_kafka_and_forward_to_pubsub():
    """Consume messages from Kafka and forward them to Pub/Sub."""
    try:
        while True:
            msg = consumer.poll(1.0)  # Poll with 1-second timeout
            if msg is None:
                continue  # No message received

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    logging.info(f"End of partition: {msg.topic()} {msg.partition()} {msg.offset()}")
                else:
                    logging.error(f"Kafka error: {msg.error()}")
                continue

            # Decode the Kafka message
            message_value = msg.value().decode('utf-8')
            logging.info(f"Received message from Kafka: {message_value[:50]}...")  # Log first 50 chars

            # Publish to Pub/Sub
            publish_to_pubsub(message_value)

    except KeyboardInterrupt:
        logging.info("Interrupted. Closing Kafka consumer.")
    finally:
        consumer.close()

def main():
    # Multi-threaded Kafka consumer to Pub/Sub
    logging.info("Starting Kafka-to-Pub/Sub connector...")

    # Use ThreadPoolExecutor for multi-threaded Kafka consumption
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(consume_kafka_and_forward_to_pubsub) for _ in range(4)]
        # Wait for all threads to complete (or exit on interrupt)
        try:
            while True:
                time.sleep(1)  # Keep the main thread alive
        except KeyboardInterrupt:
            logging.info("Shutting down threads...")

if __name__ == "__main__":
    main()
