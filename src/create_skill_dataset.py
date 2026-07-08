import pandas as pd

df = pd.read_csv("data/processed/reddit_posts_final.csv")

df = df[df["skill"] != "Unknown"].copy()

df["skill"] = df["skill"].str.split(", ")

skill_df = df.explode("skill")

skill_df.to_csv(
    "data/processed/skills_dataset.csv",
    index=False
)

print("Normalized Skills Dataset Created")
print(skill_df.head())