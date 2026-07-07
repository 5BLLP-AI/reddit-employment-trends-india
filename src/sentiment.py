import pandas as pd

from nltk.sentiment import SentimentIntensityAnalyzer

import nltk

nltk.download("vader_lexicon")


def load_dataset():

    return pd.read_csv(
        "data/processed/reddit_posts_cleaned.csv"
    )


def analyze_sentiment(text):

    sia = SentimentIntensityAnalyzer()

    score = sia.polarity_scores(text)

    compound = score["compound"]

    if compound >= 0.05:
        sentiment = "Positive"

    elif compound <= -0.05:
        sentiment = "Negative"

    else:
        sentiment = "Neutral"

    return sentiment, compound


def main():

    df = load_dataset()

    sentiments = df["clean_title"].apply(
        analyze_sentiment
    )

    df["sentiment"] = sentiments.apply(
        lambda x: x[0]
    )

    df["sentiment_score"] = sentiments.apply(
        lambda x: x[1]
    )

    df.to_csv(
        "data/processed/reddit_posts_sentiment.csv",
        index=False
    )

    print("="*60)
    print("Sentiment Analysis Completed")
    print("="*60)

    print(df[
        [
            "clean_title",
            "sentiment",
            "sentiment_score"
        ]
    ].head(20))

    print("\n")

    print(df["sentiment"].value_counts())


if __name__ == "__main__":

    main()