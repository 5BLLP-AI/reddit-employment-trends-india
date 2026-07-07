import pandas as pd


def load_dataset():

    df = pd.read_csv(
        "data/processed/reddit_posts_sentiment.csv"
    )

    return df


def preprocess_date(df):

    df["timestamp"] = pd.to_datetime(
        df["timestamp"]
    )

    df["year"] = df["timestamp"].dt.year

    df["month"] = df["timestamp"].dt.month

    df["month_name"] = df["timestamp"].dt.strftime("%b")

    return df


def print_summary(df):

    print("="*60)

    print("DATA SUMMARY")

    print("="*60)

    print("\nTop Roles\n")

    print(
        df["role"].value_counts().head(10)
    )

    print("\nTop Skills\n")

    print(
        df["skill"].value_counts().head(10)
    )

    print("\nTop Locations\n")

    print(
        df["location"].value_counts().head(10)
    )

    print("\nSentiments\n")

    print(
        df["sentiment"].value_counts()
    )


def main():

    df = load_dataset()

    df = preprocess_date(df)

    print_summary(df)

    df.to_csv(

        "data/processed/reddit_posts_trend.csv",

        index=False

    )


if __name__ == "__main__":

    main()