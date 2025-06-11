from kafka import KafkaConsumer
import json
import pandas as pd

consumer = KafkaConsumer(
    'tweet-stream',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for msg in consumer:
    tweet = msg.value
    print("Received:", tweet)
    df = pd.DataFrame([tweet])
    df.to_csv('data/streamed_tweets.csv', mode='a', header=False, index=False)
