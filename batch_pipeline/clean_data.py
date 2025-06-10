import pandas as pd

# Load raw posts
df = pd.read_csv("../data_generator/simulated_posts.csv")

# Drop rows with missing content
df_cleaned = df.dropna(subset=["content"])

# Save to cleaned CSV
df_cleaned.to_csv("cleaned_posts.csv", index=False)

print(f"Cleaned data saved. Total posts: {len(df_cleaned)}")
