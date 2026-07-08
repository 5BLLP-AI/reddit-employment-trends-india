import pandas as pd

df = pd.read_csv("data/processed/reddit_posts_featured.csv")

LOCATIONS = {

    "Bangalore":[
        "bangalore",
        "bengaluru"
    ],

    "Hyderabad":[
        "hyderabad"
    ],

    "Pune":[
        "pune"
    ],

    "Mumbai":[
        "mumbai"
    ],

    "Delhi":[
        "delhi",
        "new delhi"
    ],

    "Noida":[
        "noida"
    ],

    "Gurgaon":[
        "gurgaon",
        "gurugram"
    ],

    "Chennai":[
        "chennai"
    ],

    "Kolkata":[
        "kolkata"
    ],

    "Ahmedabad":[
        "ahmedabad"
    ],

    "Remote":[
        "remote",
        "work from home",
        "wfh"
    ]
}

def extract_location(text):

    text = str(text).lower()

    found = []

    for city, words in LOCATIONS.items():

        for word in words:

            if word in text:
                found.append(city)
                break

    if len(found)==0:
        return "Unknown"

    return ", ".join(sorted(found))

df["location"] = df["clean_title"].apply(extract_location)

df.to_csv(
    "data/processed/reddit_posts_final.csv",
    index=False
)

print("Location Normalization Complete")
print(df[["clean_title","skill","role","location"]].head())