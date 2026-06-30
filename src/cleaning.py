import pandas as pd
import re


def clean_text(text):
    if pd.isna(text):
        return ""

    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def main():

    df = pd.read_csv("data/raw/reddit_posts.csv")

    print(df.head())

    df["clean_title"] = df["title"].apply(clean_text)

    print(df[["title", "clean_title"]].head(10))

    df.drop_duplicates(inplace=True)

    print(df.isnull().sum())

    df.dropna(subset=["title"], inplace=True)

    df.to_csv(
        "data/processed/reddit_posts_cleaned.csv",
        index=False
    )

    print("=" * 40)
    print("Cleaning Completed Successfully!")
    print(f"Total Records: {len(df)}")
    print("Saved to: data/processed/reddit_posts_cleaned.csv")
    print("=" * 40)


if __name__ == "__main__":
    main()