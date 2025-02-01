from confluent_kafka import Producer
import csv
import time

# Configuration
KAFKA_BROKER = 'localhost:9092'  # Kafka broker address
KAFKA_TOPIC = 'kafkaTopic_final_1'  # Kafka topic to send data to
CSV_FILE_PATH = 'DataSet.csv'  # Path to the CSV file (update this with your actual path)

# Initialize the Kafka Producer with optimized configurations
confg = {
    'bootstrap.servers': KAFKA_BROKER,
    'queue.buffering.max.messages': 1000000,
    'queue.buffering.max.kbytes': 1048576,
    'batch.num.messages': 10000,
    'linger.ms': 1000,
    'message.max.bytes': 1048576,
    'retries': 3,
    'retry.backoff.ms': 500,
    'compression.codec': 'gzip',
}
producer = Producer(**confg)

# Callback to confirm delivery
def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result. """
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def send_data_to_kafka(csv_file_path):
    """
    Reads data from the CSV file and sends it to the specified Kafka topic.
    :param csv_file_path: Path to the CSV file to read data from
    """
    try:
        # Open and read the CSV file
        with open(csv_file_path, 'r') as file:
            csv_reader = csv.reader(file)

            # Skip the header row if the CSV has a header
            next(csv_reader)

            # Read each row and send to Kafka
            for row in csv_reader:
                message = ','.join(row)
                
                try:
                    # Send the message to the Kafka topic
                    producer.produce(KAFKA_TOPIC, value=message.encode('utf-8'), callback=delivery_report)
                except BufferError:
                    print("Buffer full, waiting for free space.")
                    producer.flush()  # Flush if the buffer is full
                    time.sleep(0.1)  # Sleep briefly to avoid busy-waiting
                    producer.produce(KAFKA_TOPIC, value=message.encode('utf-8'), callback=delivery_report)
                
                # Poll to handle delivery reports and free up queue space
                producer.poll(0)

        # Ensure all messages are sent
        producer.flush()
        print(f"All data from '{csv_file_path}' has been sent to Kafka topic '{KAFKA_TOPIC}'.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function to send data to Kafka
send_data_to_kafka(CSV_FILE_PATH)

