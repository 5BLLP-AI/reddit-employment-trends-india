import pandas as pd

df = pd.read_csv(
    "data/processed/reddit_posts_cleaned.csv"
)

print("=" * 50)
print("DATASET SUMMARY")
print("=" * 50)

print(f"Total Records : {len(df)}")
print(f"Total Columns : {len(df.columns)}")

print("\nColumns:")
print(df.columns.tolist())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("\nTop Subreddits")

print(
    df["subreddit"]
    .value_counts()
)

print("\nTop Roles")

print(
    df["role"]
    .value_counts()
)

print("\nTop Skills")

print(
    df["skill"]
    .value_counts()
)

print("\nTop Locations")

print(
    df["location"]
    .value_counts()
)

with open(
    "reports/data_quality_report.txt",
    "w"
) as file:

    file.write("DATA QUALITY REPORT\n")
    file.write("=" * 40 + "\n")

    file.write(
        f"Total Records : {len(df)}\n"
    )

    file.write(
        f"Total Columns : {len(df.columns)}\n"
    )

    file.write("\nMissing Values\n")

    file.write(
        str(df.isnull().sum())
    )

    file.write("\n\nDuplicate Rows\n")

    file.write(
        str(df.duplicated().sum())
    )