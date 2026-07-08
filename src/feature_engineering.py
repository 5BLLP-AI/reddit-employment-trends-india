import pandas as pd

# ==========================
# LOAD DATA
# ==========================

df = pd.read_csv("data/processed/reddit_posts_cleaned.csv")

# ==========================
# SKILLS DICTIONARY
# ==========================

SKILLS = {
    "Python": [
        "python", "django", "flask", "fastapi", "pandas",
        "numpy", "matplotlib", "opencv", "streamlit"
    ],

    "Java": [
        "java", "spring", "spring boot"
    ],

    "JavaScript": [
        "javascript", "js", "node", "nodejs",
        "react", "angular", "vue", "nextjs", "next.js"
    ],

    "SQL": [
        "sql", "mysql", "postgres", "postgresql",
        "sqlite", "oracle", "sql server"
    ],

    "Cloud": [
        "aws", "azure", "gcp", "cloud"
    ],

    "Machine Learning": [
        "machine learning",
        "ml",
        "scikit",
        "sklearn",
        "xgboost"
    ],

    "Artificial Intelligence": [
        "ai",
        "artificial intelligence",
        "llm",
        "gpt",
        "chatgpt",
        "generative ai",
        "gen ai"
    ],

    "Data Science": [
        "data science",
        "data scientist"
    ],

    "DevOps": [
        "docker",
        "kubernetes",
        "jenkins",
        "terraform",
        "ansible"
    ],

    "Git": [
        "git",
        "github",
        "gitlab"
    ],

    "C++": [
        "c++",
        "cpp"
    ],

    "C": [
        " c ",
        " c,"
    ]
}

# ==========================
# ROLE DICTIONARY
# ==========================

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
        "react developer"
    ],

    "Full Stack Developer":[
        "full stack",
        "fullstack",
        "mern",
        "mean"
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

    "DevOps Engineer":[
        "devops engineer"
    ],

    "Intern":[
        "intern",
        "internship",
        "summer intern"
    ]
}

# ==========================
# SKILL EXTRACTION
# ==========================

def extract_skills(text):

    text = str(text).lower()

    found = []

    for skill, words in SKILLS.items():

        for word in words:

            if word in text:
                found.append(skill)
                break

    return sorted(list(set(found)))

# ==========================
# ROLE EXTRACTION
# ==========================

def extract_role(text):

    text = str(text).lower()

    for role, words in ROLES.items():

        for word in words:

            if word in text:
                return role

    return "Unknown"

# ==========================
# APPLY
# ==========================

df["skills_list"] = df["clean_title"].apply(extract_skills)

df["skill"] = df["skills_list"].apply(
    lambda x: ", ".join(x) if len(x) else "Unknown"
)

df["role"] = df["clean_title"].apply(extract_role)

# ==========================
# SAVE
# ==========================

df.to_csv(
    "data/processed/reddit_posts_featured.csv",
    index=False
)

print("Feature Engineering Complete")
print(df[["clean_title","skill","role"]].head())