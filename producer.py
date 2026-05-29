import json
import random
import time
from datetime import datetime, timedelta
from kafka import KafkaProducer

# Kafka configuration
KAFKA_TOPIC = "train_schedule_data"

KAFKA_SERVER = "localhost:9092"

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# List of different train names and their routes
train_info = [
    {"train_name": "Rajdhani Express", "source": "Delhi", "destination": "Mumbai"},
    {"train_name": "Shatabdi Express", "source": "Chennai", "destination": "Bangalore"},
    {"train_name": "Duronto Express", "source": "Kolkata", "destination": "Delhi"},
    {"train_name": "Garib Rath Express", "source": "Hyderabad", "destination": "Vishakhapatnam"},
    {"train_name": "Tejas Express", "source": "Ahmedabad", "destination": "Surat"},
    {"train_name": "Jan Shatabdi Express", "source": "Lucknow", "destination": "Varanasi"},
    {"train_name": "Vande Bharat Express", "source": "Delhi", "destination": "Varanasi"},
    {"train_name": "Humsafar Express", "source": "Mumbai", "destination": "Lucknow"},
    {"train_name": "Sampark Kranti Express", "source": "Bhopal", "destination": "Delhi"},
    {"train_name": "Karnataka Express", "source": "Bangalore", "destination": "Delhi"},
    {"train_name": "Maharaja Express", "source": "Delhi", "destination": "Jaipur"},
    {"train_name": "Deccan Queen", "source": "Mumbai", "destination": "Pune"},
    {"train_name": "Konkan Express", "source": "Goa", "destination": "Mumbai"},
    {"train_name": "Purushottam Express", "source": "Puri", "destination": "Delhi"},
    {"train_name": "Nanda Devi Express", "source": "Dehradun", "destination": "Delhi"},
    {"train_name": "Utkal Express", "source": "Puri", "destination": "Haridwar"},
    {"train_name": "Tamil Nadu Express", "source": "Chennai", "destination": "Delhi"},
    {"train_name": "Andhra Pradesh Express", "source": "Hyderabad", "destination": "Delhi"},
    {"train_name": "Kerala Express", "source": "Trivandrum", "destination": "Delhi"},
    {"train_name": "Ganga Sutlej Express", "source": "Dhanbad", "destination": "Ludhiana"},
    {"train_name": "Kashi Vishwanath Express", "source": "Varanasi", "destination": "Delhi"},
    {"train_name": "Rameswaram Express", "source": "Madurai", "destination": "Rameswaram"},
    {"train_name": "Ajmer Shatabdi", "source": "Delhi", "destination": "Ajmer"},
    {"train_name": "Mandovi Express", "source": "Goa", "destination": "Mumbai"},
    {"train_name": "Hawrah Express", "source": "Howrah", "destination": "Ahmedabad"},
    {"train_name": "Gorakhpur Express", "source": "Mumbai", "destination": "Gorakhpur"},
    {"train_name": "Chalukya Express", "source": "Pune", "destination": "Bangalore"},
    {"train_name": "Jammu Tawi Express", "source": "Jammu", "destination": "Delhi"},
    {"train_name": "Mumbai Express", "source": "Chennai", "destination": "Mumbai"},
    {"train_name": "Jnaneshwari Express", "source": "Mumbai", "destination": "Howrah"},
    {"train_name": "Bhagat Ki Kothi Express", "source": "Jodhpur", "destination": "Bangalore"},
    {"train_name": "Hazrat Nizamuddin Express", "source": "Delhi", "destination": "Chennai"},
    {"train_name": "Amritsar Express", "source": "Amritsar", "destination": "Delhi"},
    {"train_name": "Hyderabad Express", "source": "Chennai", "destination": "Hyderabad"},
    {"train_name": "Sealdah Express", "source": "Kolkata", "destination": "Delhi"},
    {"train_name": "Bhubaneswar Express", "source": "Bhubaneswar", "destination": "Bangalore"},
    {"train_name": "Raptisagar Express", "source": "Trivandrum", "destination": "Gorakhpur"},
    {"train_name": "Navjeevan Express", "source": "Chennai", "destination": "Ahmedabad"},
    {"train_name": "Yeshwantpur Express", "source": "Bangalore", "destination": "Delhi"},
    {"train_name": "Howrah Rajdhani", "source": "Howrah", "destination": "Delhi"},
    {"train_name": "Kanyakumari Express", "source": "Kanyakumari", "destination": "Mumbai"},
    {"train_name": "Lucknow Mail", "source": "Delhi", "destination": "Lucknow"},
    {"train_name": "Palace on Wheels", "source": "Delhi", "destination": "Rajasthan"},
    {"train_name": "Nilgiri Express", "source": "Chennai", "destination": "Mettupalayam"},
    {"train_name": "Dibrugarh Express", "source": "Dibrugarh", "destination": "Delhi"},
    {"train_name": "Jalna Express", "source": "Mumbai", "destination": "Jalna"},
    {"train_name": "Bidar Express", "source": "Hyderabad", "destination": "Bidar"},
    {"train_name": "Panchavati Express", "source": "Mumbai", "destination": "Nashik"}
]

# Generate random train timing data
def generate_train_data(train):
    departure_time = datetime.now() + timedelta(minutes=random.randint(10, 120))
    arrival_time = departure_time + timedelta(hours=random.randint(5, 12))

    data = {
        "train_number": random.randint(10000, 99999),
        "train_name": train["train_name"],
        "source": train["source"],
        "destination": train["destination"],
        "departure_time": departure_time.strftime("%Y-%m-%d %H:%M:%S"),
        "arrival_time": arrival_time.strftime("%Y-%m-%d %H:%M:%S"),
        "platform": random.randint(1, 10),
        "status": random.choice(["On Time", "Delayed", "Cancelled"]),
        "timestamp": datetime.now().isoformat()
    }

    return data

# Produce data to Kafka every 5 seconds
while True:
    train = random.choice(train_info)
    train_data = generate_train_data(train)
    producer.send(KAFKA_TOPIC, value=train_data)
    print(f"Sent: {train_data}")
    time.sleep(5)