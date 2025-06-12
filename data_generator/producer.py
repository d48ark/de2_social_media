from kafka import KafkaProducer
import json
import time
import pandas as pd

KAFKA_TOPIC = "social-media"
KAFKA_SERVER = "localhost:9092"

# Kafka producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# Load Faker data
df = pd.read_csv("simulated_posts.csv")
df = df.dropna(subset=['content'])  # remove empty content

for _, row in df.iterrows():
    post = {
        "user": row["user_id"],
        "text": row["content"],
        "timestamp": row["timestamp"],
        "location": row["location"],
        "platform": row["platform"]
    }
    producer.send(KAFKA_TOPIC, post)
    print(f"Sent: {post}")
    time.sleep(0.2)  # can be reduced for faster stream

producer.flush()
