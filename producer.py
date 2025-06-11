from kafka import KafkaProducer
import json, time
import random

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

messages = [
    {"id": 1, "text": "I love this!", "created_at": "2025-06-10T12:00:00"},
    {"id": 2, "text": None, "created_at": "2025-06-10T12:00:10"},  # Missing text
    {"id": 3, "text": "Great", "created_at": "2025-06-10T12:00:20"},
    {"id": 3, "text": "Great", "created_at": "2025-06-10T12:00:20"},  # Duplicate
    {"id": 4, "text": "Worst ever!!!", "created_at": "9999-99-99T99:99:99"},  # Timestamp outlier
]


sample_data = [
    {"id": 1, "text": "Love this product!", "created_at": "2025-06-10T12:00:00"},
    {"id": 2, "text": "", "created_at": "2025-06-10T12:01:00"},
    {"id": 3, "text": "Not bad", "created_at": "2025-06-10T12:01:10"},
    {"id": 1, "text": "Love this product!", "created_at": "2025-06-10T12:00:00"},
    {"id": 4, "text": "Worst ever!!!", "created_at": "9999-99-99T99:99:99"}
]

while True:
    tweet = random.choice(sample_data)
    producer.send('tweet-stream', tweet)
    print("Sent:", tweet)
    time.sleep(2)
