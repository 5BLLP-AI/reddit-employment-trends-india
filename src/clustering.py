import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


def load_dataset():

    return pd.read_csv(
        "data/processed/reddit_posts_cleaned.csv"
    )


def create_text(df):

    return (
        df["keyword"].fillna("") +
        " " +
        df["clean_title"].fillna("")
    )


def build_tfidf(text):

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=1500
    )

    matrix = vectorizer.fit_transform(text)

    return matrix, vectorizer


def train_clusters(matrix):

    model = KMeans(
        n_clusters=5,
        random_state=42,
        n_init=10
    )

    labels = model.fit_predict(matrix)

    return model, labels


def main():

    df = load_dataset()

    text = create_text(df)

    matrix, vectorizer = build_tfidf(text)

    model, labels = train_clusters(matrix)

    df["cluster"] = labels

    df.to_csv(
        "data/processed/reddit_posts_clustered.csv",
        index=False
    )

    print("="*60)
    print("CLUSTERING COMPLETED")
    print("="*60)

    print(df["cluster"].value_counts())

if __name__ == "__main__":
    main()