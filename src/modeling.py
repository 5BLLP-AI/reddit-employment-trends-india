import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer


def load_dataset():

    df = pd.read_csv(
        "data/processed/reddit_posts_cleaned.csv"
    )

    return df


def build_tfidf(text_column):

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=1000
    )

    tfidf_matrix = vectorizer.fit_transform(
        text_column
    )

    return tfidf_matrix, vectorizer


def get_top_words(tfidf_matrix, vectorizer, top_n=20):

    scores = tfidf_matrix.sum(axis=0).A1

    words = vectorizer.get_feature_names_out()

    importance = pd.DataFrame({

        "word": words,

        "score": scores

    })

    importance = importance.sort_values(

        by="score",

        ascending=False

    )

    return importance.head(top_n)


def main():

    df = load_dataset()

    tfidf_matrix, vectorizer = build_tfidf(

        df["clean_title"]

    )

    top_words = get_top_words(

        tfidf_matrix,

        vectorizer,

        top_n=20

    )

    print("=" * 60)

    print("TOP TF-IDF WORDS")

    print("=" * 60)

    print(top_words)


if __name__ == "__main__":

    main()