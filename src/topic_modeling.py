import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation


def load_dataset():

    return pd.read_csv(
        "data/processed/reddit_posts_cleaned.csv"
    )


def prepare_text(df):

    return (
        df["keyword"].fillna("") +
        " " +
        df["clean_title"].fillna("")
    )


def build_bow(text):

    vectorizer = CountVectorizer(

        stop_words="english",

        max_features=1000

    )

    matrix = vectorizer.fit_transform(text)

    return matrix, vectorizer


def train_lda(matrix):

    lda = LatentDirichletAllocation(

        n_components=5,

        random_state=42

    )

    topics = lda.fit_transform(matrix)

    return lda, topics


def print_topics(model, vectorizer):

    words = vectorizer.get_feature_names_out()

    for idx, topic in enumerate(model.components_):

        print("=" * 60)

        print(f"Topic {idx+1}")

        top = topic.argsort()[-10:][::-1]

        print(

            ", ".join(

                words[i]

                for i in top

            )

        )


def main():

    df = load_dataset()

    text = prepare_text(df)

    matrix, vectorizer = build_bow(text)

    lda, topics = train_lda(matrix)

    df["topic"] = topics.argmax(axis=1)

    df.to_csv(

        "data/processed/reddit_posts_topics.csv",

        index=False

    )

    print_topics(

        lda,

        vectorizer

    )


if __name__ == "__main__":

    main()