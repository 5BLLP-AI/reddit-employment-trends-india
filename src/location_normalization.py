import pandas as pd

df = pd.read_csv(
    "data/processed/reddit_posts_cleaned.csv"
)

LOCATIONS = {
    "bangalore": "Bangalore",
    "bengaluru": "Bangalore",
    "hyderabad": "Hyderabad",
    "pune": "Pune",
    "mumbai": "Mumbai",
    "delhi": "Delhi",
    "gurgaon": "Gurugram",
    "gurugram": "Gurugram",
    "noida": "Noida",
    "chennai": "Chennai",
    "kolkata": "Kolkata",
    "ahmedabad": "Ahmedabad",
    "kochi": "Kochi",
    "trivandrum": "Thiruvananthapuram",
    "jaipur": "Jaipur",
    "indore": "Indore"
}

def extract_location(text):

    text = str(text).lower()

    for city in LOCATIONS:

        if city in text:

            return LOCATIONS[city]

    return "Unknown"

df["location"] = df["clean_title"].apply(
    extract_location
)

print(
    df[
        ["clean_title", "location"]
    ].head(20)
)

print(
    df["location"].value_counts()
)

df.to_csv(
    "data/processed/reddit_posts_cleaned.csv",
    index=False
)

print("=" * 40)
print("Location Extraction Completed!")
print(f"Rows Processed: {len(df)}")
print("=" * 40)
