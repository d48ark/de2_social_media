from kafka import KafkaConsumer
import json
import pandas as pd
import time
from datetime import datetime
import os
import pickle

# === Create Folder (for CSV) ===
os.makedirs("data", exist_ok=True)

# === Load ML Model ===
with open("spam_model.pkl", "rb") as f:
    spam_model = pickle.load(f)

# === Settings ===
TOPIC_NAME = 'social-media'
BOOTSTRAP_SERVER = 'localhost:9092'
BATCH_DURATION = 10  # seconds

# === Kafka Consumer Definition ===
consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=BOOTSTRAP_SERVER,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='stream-analytics-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print(f"[{datetime.now()}] Kafka consumer started. Micro-batch duration: {BATCH_DURATION} seconds.")

# === Micro-Batch Loop ===
batch = []
start_time = time.time()

try:
    for msg in consumer:
        tweet = msg.value
        batch.append(tweet)

        if time.time() - start_time >= BATCH_DURATION:
            print(f"\n[{datetime.now()}] --- Processing New Micro-Batch ({len(batch)} tweets) ---")

            if batch:
                df = pd.DataFrame(batch)

                # === Analytics ===
                total_tweets = len(df)
                avg_length = df['text'].apply(len).mean()
                long_tweets = df[df['text'].apply(len) > 100]

                print(f"Total number of tweets: {total_tweets}")
                print(f"Average tweet length: {avg_length:.2f} characters")

                if not long_tweets.empty:
                    print("⚠️ Long tweets (100+ characters):")
                    for idx, row in long_tweets.iterrows():
                        print(f"- @{row['user']}: {row['text']}")

                # === Spam Prediction ===
                df['is_spam'] = spam_model.predict(df['text'])

                print("\nSpam analysis result:")
                for idx, row in df.iterrows():
                    print(f"@{row['user']} → SPAM: {bool(row['is_spam'])} | {row['text']}")

                # === Save to CSV ===
                df.to_csv('data/streamed_tweets.csv', mode='a', header=not os.path.exists('data/streamed_tweets.csv'), index=False)

            # Reset batch
            batch = []
            start_time = time.time()

except KeyboardInterrupt:
    print("\n❗ Process interrupted by user.")

except Exception as e:
    print(f"🚨 An error occurred: {e}")
