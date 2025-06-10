import pandas as pd

# Load cleaned posts
df = pd.read_csv("cleaned_posts.csv")

# Convert timestamp to datetime
df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')

# Round to the nearest hour
df["hour"] = df["timestamp"].dt.floor("H")

# Aggregate: average sentiment per hour
agg_df = df.groupby("hour")["sentiment_score"].mean().reset_index()
agg_df.columns = ["hour", "average_sentiment"]

# Save output
agg_df.to_csv("hourly_sentiment.csv", index=False)

print("Hourly sentiment aggregation saved.")
