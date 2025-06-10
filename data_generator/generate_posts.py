from faker import Faker
import pandas as pd
import random
import uuid
from datetime import datetime, timedelta

fake = Faker()
platforms = ["Twitter", "Reddit", "Facebook"]
sentiments = [-1, 0, 1]  # optional, can label manually later

def generate_post():
    return {
        "post_id": str(uuid.uuid4()),
        "user_id": fake.user_name(),
        "content": fake.sentence(nb_words=random.randint(5, 15)),
        "timestamp": datetime.utcnow().isoformat(),
        "location": fake.city(),
        "platform": random.choice(platforms),
        "sentiment_score": random.choice(sentiments)
    }

def generate_posts(hour_count=6, posts_per_hour=1000):
    all_posts = []
    for hour in range(hour_count):
        for _ in range(posts_per_hour):
            post = generate_post()
            # Inject noise
            if random.random() < 0.02: post["content"] = None  # missing content
            if random.random() < 0.01: all_posts.append(post)  # duplicate
            all_posts.append(post)
    return pd.DataFrame(all_posts)

if __name__ == "__main__":
    df = generate_posts()
    df.to_csv("simulated_posts.csv", index=False)
    print(f"Generated {len(df)} posts.")
