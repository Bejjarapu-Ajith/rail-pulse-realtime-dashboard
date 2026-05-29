import json
from kafka import KafkaConsumer

# Kafka configuration
KAFKA_TOPIC = "train_schedule_data"
KAFKA_SERVER = "localhost:9092"

# Initialize Kafka consumer
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_SERVER,
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    auto_offset_reset='earliest',  # Start consuming from the beginning if no offset is committed
    enable_auto_commit=True
)

print(f"Listening for messages on topic '{KAFKA_TOPIC}'...\n")

# Consume messages continuously
for message in consumer:
    train_data = message.value
    
    # Extracting required fields
    train_number = train_data.get('train_number', 'Unknown')
    train_name = train_data.get('train_name', 'Unknown')
    source = train_data.get('source', 'Unknown')
    destination = train_data.get('destination', 'Unknown')
    departure_time = train_data.get('departure_time', 'Unknown')
    arrival_time = train_data.get('arrival_time', 'Unknown')
    platform = train_data.get('platform', 'Unknown')
    status = train_data.get('status', 'Unknown')
    timestamp = train_data.get('timestamp', 'Unknown')

    # Display train information in the required format
    print(f"Train Number: {train_number}")
    print(f"Train Name: {train_name}")
    print(f"Source: {source}")
    print(f"Destination: {destination}")
    print(f"Departure Time: {departure_time}")
    print(f"Arrival Time: {arrival_time}")
    print(f"Platform: {platform}")
    print(f"Status: {status}")
    print(f"Timestamp: {timestamp}")
    print("-" * 50)  # Separator for better readability
