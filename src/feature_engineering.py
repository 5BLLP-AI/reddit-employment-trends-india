import pandas as pd

# =====================================================
# Load Cleaned Dataset
# =====================================================

df = pd.read_csv(
    "data/processed/reddit_posts_cleaned.csv"
)

# =====================================================
# SKILL DICTIONARY
# =====================================================

SKILLS = {

    "Python":[
        "python","django","flask","fastapi","pandas","numpy",
        "scikit","scikit-learn","pytorch","tensorflow",
        "opencv","matplotlib","seaborn","streamlit"
    ],

    "Java":[
        "java","spring","spring boot","hibernate","maven","gradle"
    ],

    "JavaScript":[
        "javascript","js","node","nodejs","express",
        "react","reactjs","angular","vue","nextjs",
        "typescript"
    ],

    "C++":[
        "c++","cpp","stl"
    ],

    "C":[
        "c programming","embedded c"
    ],

    "SQL":[
        "sql","mysql","postgres","postgresql",
        "sqlite","oracle","sql server"
    ],

    "NoSQL":[
        "mongodb","cassandra","redis","firebase"
    ],

    "Cloud":[
        "aws","amazon web services",
        "azure","gcp",
        "google cloud",
        "cloud"
    ],

    "Machine Learning":[
        "machine learning",
        "ml",
        "xgboost",
        "lightgbm",
        "catboost"
    ],

    "Artificial Intelligence":[
        "ai",
        "artificial intelligence",
        "llm",
        "gpt",
        "chatgpt",
        "generative ai",
        "gen ai",
        "langchain",
        "llamaindex",
        "rag"
    ],

    "Data Science":[
        "data science",
        "data scientist",
        "statistics",
        "analytics"
    ],

    "Data Engineering":[
        "airflow",
        "spark",
        "pyspark",
        "hadoop",
        "kafka",
        "etl",
        "data pipeline"
    ],

    "DevOps":[
        "docker",
        "kubernetes",
        "jenkins",
        "terraform",
        "ansible",
        "devops"
    ],

    "Git":[
        "git",
        "github",
        "gitlab",
        "bitbucket"
    ],

    "Linux":[
        "linux",
        "ubuntu",
        "unix",
        "bash",
        "shell"
    ],

    "Networking":[
        "tcp",
        "udp",
        "http",
        "dns",
        "networking"
    ]
}

# =====================================================
# ROLE DICTIONARY
# =====================================================

ROLES = {

    "Software Engineer":[
        "software engineer",
        "software developer",
        "developer",
        "programmer",
        "sde"
    ],

    "Backend Developer":[
        "backend",
        "backend developer",
        "backend engineer"
    ],

    "Frontend Developer":[
        "frontend",
        "frontend developer",
        "frontend engineer",
        "ui developer"
    ],

    "Full Stack Developer":[
        "full stack",
        "fullstack",
        "full stack developer"
    ],

    "Web Developer":[
        "web developer",
        "website developer"
    ],

    "Mobile Developer":[
        "android developer",
        "ios developer",
        "flutter developer",
        "react native"
    ],

    "Data Scientist":[
        "data scientist"
    ],

    "Data Analyst":[
        "data analyst",
        "business analyst"
    ],

    "Machine Learning Engineer":[
        "machine learning engineer",
        "ml engineer"
    ],

    "AI Engineer":[
        "ai engineer",
        "llm engineer",
        "gen ai engineer"
    ],

    "Data Engineer":[
        "data engineer",
        "etl developer"
    ],

    "DevOps Engineer":[
        "devops engineer",
        "site reliability engineer",
        "sre"
    ],

    "Cloud Engineer":[
        "cloud engineer"
    ],

    "QA Engineer":[
        "qa",
        "quality assurance",
        "test engineer"
    ],

    "Security Engineer":[
        "cyber security",
        "security engineer",
        "penetration tester"
    ],

    "Intern":[
        "intern",
        "internship",
        "summer intern"
    ],

    "Fresher":[
        "fresher",
        "entry level",
        "graduate engineer trainee",
        "get"
    ]
}

# =====================================================
# SKILL EXTRACTION
# =====================================================

def extract_skill(text):

    if pd.isna(text):
        return "Unknown"

    text = text.lower()

    found = []

    for skill, words in SKILLS.items():

        for word in words:

            if word in text:

                found.append(skill)
                break

    if found:

        return ", ".join(sorted(set(found)))

    return "Unknown"

# =====================================================
# ROLE EXTRACTION
# =====================================================

def extract_role(text):

    if pd.isna(text):
        return "Unknown"

    text = text.lower()

    found = []

    for role, words in ROLES.items():

        for word in words:

            if word in text:

                found.append(role)
                break

    if found:

        return ", ".join(sorted(set(found)))

    return "Unknown"

# =====================================================
# APPLY FEATURE ENGINEERING
# =====================================================

df["skill"] = df["clean_title"].apply(
    extract_skill
)

df["role"] = df["clean_title"].apply(
    extract_role
)

combined_text = (
    df["keyword"].fillna("") +
    " " +
    df["clean_title"].fillna("")
)

df["skill"] = combined_text.apply(extract_skill)
df["role"] = combined_text.apply(extract_role)

# =====================================================
# SAVE DATASET
# =====================================================

df.to_csv(
    "data/processed/reddit_posts_cleaned.csv",
    index=False
)

# =====================================================
# SUMMARY
# =====================================================

print("="*60)
print("FEATURE ENGINEERING COMPLETED")
print("="*60)

print("\nSample Output\n")

print(
    df[
        [
            "clean_title",
            "skill",
            "role"
        ]
    ].head(20)
)

print("\nTop Skills\n")
print(df["skill"].value_counts().head(20))

print("\nTop Roles\n")
print(df["role"].value_counts().head(20))

print("\nDataset Saved Successfully")