import pandas as pd

# ===========================================================
# LOCATION DICTIONARY
# ===========================================================

LOCATION_KEYWORDS = {

    "Bangalore": [
        "bangalore",
        "bengaluru"
    ],

    "Hyderabad": [
        "hyderabad"
    ],

    "Pune": [
        "pune"
    ],

    "Mumbai": [
        "mumbai",
        "bombay",
        "navi mumbai"
    ],

    "Delhi": [
        "delhi",
        "new delhi"
    ],

    "Noida": [
        "noida",
        "greater noida"
    ],

    "Gurgaon": [
        "gurgaon",
        "gurugram"
    ],

    "Chennai": [
        "chennai",
        "madras"
    ],

    "Kolkata": [
        "kolkata",
        "calcutta"
    ],

    "Ahmedabad": [
        "ahmedabad"
    ],

    "Jaipur": [
        "jaipur"
    ],

    "Lucknow": [
        "lucknow"
    ],

    "Kanpur": [
        "kanpur"
    ],

    "Indore": [
        "indore"
    ],

    "Bhopal": [
        "bhopal"
    ],

    "Nagpur": [
        "nagpur"
    ],

    "Surat": [
        "surat"
    ],

    "Vadodara": [
        "vadodara",
        "baroda"
    ],

    "Rajkot": [
        "rajkot"
    ],

    "Nashik": [
        "nashik",
        "nasik"
    ],

    "Aurangabad": [
        "aurangabad"
    ],

    "Goa": [
        "goa"
    ],

    "Kochi": [
        "kochi",
        "cochin"
    ],

    "Thiruvananthapuram": [
        "thiruvananthapuram",
        "trivandrum"
    ],

    "Kozhikode": [
        "kozhikode",
        "calicut"
    ],

    "Mysore": [
        "mysore",
        "mysuru"
    ],

    "Mangalore": [
        "mangalore",
        "mangaluru"
    ],

    "Visakhapatnam": [
        "visakhapatnam",
        "vizag"
    ],

    "Vijayawada": [
        "vijayawada"
    ],

    "Coimbatore": [
        "coimbatore"
    ],

    "Madurai": [
        "madurai"
    ],

    "Patna": [
        "patna"
    ],

    "Ranchi": [
        "ranchi"
    ],

    "Bhubaneswar": [
        "bhubaneswar"
    ],

    "Chandigarh": [
        "chandigarh"
    ],

    "Mohali": [
        "mohali"
    ],

    "Dehradun": [
        "dehradun"
    ],

    "Jammu": [
        "jammu"
    ],

    "Srinagar": [
        "srinagar"
    ],

    "Remote": [
        "remote",
        "work from home",
        "wfh",
        "anywhere",
        "remote-first",
        "fully remote"
    ],

    "Hybrid": [
        "hybrid"
    ]
}

# ===========================================================
# LOCATION EXTRACTION FUNCTION
# ===========================================================

def extract_location(text):

    if pd.isna(text):
        return "Unknown"

    text = text.lower()

    found = []

    for location, keywords in LOCATION_KEYWORDS.items():

        for keyword in keywords:

            if keyword in text:

                found.append(location)
                break

    if found:

        return ", ".join(sorted(set(found)))

    return "Unknown"

# ===========================================================
# APPLY LOCATION EXTRACTION
# ===========================================================

def normalize_locations(df):

    # Use keyword + title for better matching
    combined_text = (
        df["keyword"].fillna("") +
        " " +
        df["clean_title"].fillna("")
    )

    df["location"] = combined_text.apply(extract_location)

    return df


# ===========================================================
# MAIN
# ===========================================================

if __name__ == "__main__":

    df = pd.read_csv(
        "data/processed/reddit_posts_cleaned.csv"
    )

    df = normalize_locations(df)

    df.to_csv(
        "data/processed/reddit_posts_cleaned.csv",
        index=False
    )

    print("=" * 60)
    print("LOCATION NORMALIZATION COMPLETED")
    print("=" * 60)

    print("\nTop Locations\n")

    print(df["location"].value_counts().head(20))

    print("\nDataset Saved Successfully")