from kafka import KafkaProducer
import json
import time

KAFKA_TOPIC = "social-media"
KAFKA_SERVER = "localhost:9092"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

with open("sample_data.json", "r") as f:
    tweets = json.load(f)

for tweet in tweets:
    producer.send(KAFKA_TOPIC, tweet)
    print(f"Sent tweet: {tweet}")
    time.sleep(1)

producer.flush()

