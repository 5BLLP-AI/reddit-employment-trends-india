import pandas as pd

df = pd.read_csv("data/processed/reddit_posts_final.csv")

df = df[df["location"] != "Unknown"].copy()

df["location"] = df["location"].str.split(", ")

location_df = df.explode("location")

location_df.to_csv(
    "data/processed/location_dataset.csv",
    index=False
)

print("Normalized Location Dataset Created")
print(location_df.head())