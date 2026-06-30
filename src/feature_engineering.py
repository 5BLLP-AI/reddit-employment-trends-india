import pandas as pd

df = pd.read_csv(
    "data/processed/reddit_posts_cleaned.csv"
)

SKILLS = {

    "python": "Python",

    "java": "Java",

    "javascript": "JavaScript",

    "react": "React",

    "angular": "Angular",

    "node": "Node.js",

    "sql": "SQL",

    "mysql": "MySQL",

    "postgresql": "PostgreSQL",

    "mongodb": "MongoDB",

    "aws": "AWS",

    "azure": "Azure",

    "gcp": "Google Cloud",

    "docker": "Docker",

    "kubernetes": "Kubernetes",

    "git": "Git",

    "linux": "Linux",

    "tensorflow": "TensorFlow",

    "pytorch": "PyTorch",

    "machine learning": "Machine Learning",

    "deep learning": "Deep Learning",

    "ai": "Artificial Intelligence",

    "excel": "Excel",

    "power bi": "Power BI",

    "tableau": "Tableau"
}

ROLES = {

    "software engineer": "Software Engineer",

    "software developer": "Software Developer",

    "backend": "Backend Developer",

    "frontend": "Frontend Developer",

    "full stack": "Full Stack Developer",

    "data analyst": "Data Analyst",

    "data scientist": "Data Scientist",

    "ml engineer": "Machine Learning Engineer",

    "machine learning engineer": "Machine Learning Engineer",

    "ai engineer": "AI Engineer",

    "devops": "DevOps Engineer",

    "qa": "QA Engineer",

    "tester": "QA Engineer",

    "intern": "Intern",

    "internship": "Intern",

    "sde": "Software Development Engineer"
}

def extract_skill(text):

    text = str(text).lower()

    found = []

    for keyword, skill in SKILLS.items():

        if keyword in text:

            found.append(skill)

    if len(found) == 0:

        return "Unknown"

    return ", ".join(found)

def extract_role(text):

    text = str(text).lower()

    for keyword, role in ROLES.items():

        if keyword in text:

            return role

    return "Unknown"

df["skill"] = df["clean_title"].apply(
    extract_skill
)

df["role"] = df["clean_title"].apply(
    extract_role
)

print(
    df[
        [
            "clean_title",
            "skill",
            "role"
        ]
    ].head(20)
)

print(
    "\nTop Skills:\n"
)

print(
    df["skill"].value_counts().head(10)
)

print(
    "\nTop Roles:\n"
)

print(
    df["role"].value_counts()
)

