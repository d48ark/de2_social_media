from kafka import KafkaConsumer
import json
import pandas as pd
import time
from datetime import datetime
import os
import pickle

# === Klasör Oluştur (CSV için) ===
os.makedirs("data", exist_ok=True)

# === ML Modeli Yükle ===
with open("spam_model.pkl", "rb") as f:
    spam_model = pickle.load(f)

# === Ayarlar ===
TOPIC_NAME = 'social-media'
BOOTSTRAP_SERVER = 'localhost:9092'
BATCH_DURATION = 10  # saniye

# === Kafka Consumer Tanımı ===
consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=BOOTSTRAP_SERVER,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='stream-analytics-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print(f"[{datetime.now()}] Kafka consumer başlatıldı. Mikro-batch süresi: {BATCH_DURATION} saniye.")

# === Mikro-Batch Döngüsü ===
batch = []
start_time = time.time()

try:
    for msg in consumer:
        tweet = msg.value
        batch.append(tweet)

        if time.time() - start_time >= BATCH_DURATION:
            print(f"\n[{datetime.now()}] --- Yeni Mikro-Batch İşleniyor ({len(batch)} tweet) ---")

            if batch:
                df = pd.DataFrame(batch)

                # === Analitikler ===
                total_tweets = len(df)
                avg_length = df['text'].apply(len).mean()
                long_tweets = df[df['text'].apply(len) > 100]

                print(f"Toplam tweet sayısı: {total_tweets}")
                print(f"Ortalama tweet uzunluğu: {avg_length:.2f} karakter")

                if not long_tweets.empty:
                    print("⚠️ Uzun tweetler (100+ karakter):")
                    for idx, row in long_tweets.iterrows():
                        print(f"- @{row['user']}: {row['text']}")

                # === Spam Tahmini ===
                df['is_spam'] = spam_model.predict(df['text'])

                print("\nSpam analiz sonucu:")
                for idx, row in df.iterrows():
                    print(f"@{row['user']} → SPAM: {bool(row['is_spam'])} | {row['text']}")

                # === CSV’ye Kaydet ===
                df.to_csv('data/streamed_tweets.csv', mode='a', header=not os.path.exists('data/streamed_tweets.csv'), index=False)

            # Batch sıfırla
            batch = []
            start_time = time.time()

except KeyboardInterrupt:
    print("\n❗ İşlem kullanıcı tarafından durduruldu.")

except Exception as e:
    print(f"🚨 Hata oluştu: {e}")
