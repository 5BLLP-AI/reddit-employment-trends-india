# ===============================
# SOFTWARE ENGINEER
# ===============================

software_keywords = [

    "software engineer india",

    "software developer india",

    "backend developer india",

    "frontend developer india",

    "full stack developer india",

    "java developer india",

    "python developer india",

    "react developer india",

    "node js developer india",

    "golang developer india",

    "devops engineer india",

    "cloud engineer india",

    "aws engineer india",

    "android developer india",

    "ios developer india"

]


# ===============================
# DATA
# ===============================

data_keywords = [

    "data analyst india",

    "business analyst india",

    "data scientist india",

    "machine learning engineer india",

    "AI engineer india",

    "deep learning engineer india",

    "analytics hiring india",

    "power bi jobs india",

    "sql jobs india",

    "python data jobs india",

    "tableau jobs india",

    "big data engineer india"

]


# ===============================
# INTERNSHIPS
# ===============================

internship_keywords = [

    "software internship india",

    "AI internship india",

    "ML internship india",

    "data internship india",

    "summer internship india",

    "winter internship india",

    "college internship india",

    "web development internship",

    "python internship",

    "remote internship india"

]


# ===============================
# HIRING
# ===============================

hiring_keywords = [

    "hiring india",

    "urgent hiring",

    "we are hiring",

    "looking for developer",

    "looking for software engineer",

    "job opening india",

    "career opportunity india",

    "join our engineering team",

    "walk in interview india",

    "recruitment india"

]


# ===============================
# COMPANIES
# ===============================

company_keywords = [

    "Google hiring",

    "Microsoft hiring",

    "Amazon hiring",

    "Meta hiring",

    "Adobe hiring",

    "Oracle hiring",

    "Infosys hiring",

    "TCS hiring",

    "Wipro hiring",

    "Capgemini hiring",

    "Accenture hiring",

    "IBM hiring",

    "Cognizant hiring",

    "Flipkart hiring",

    "Paytm hiring"

]


# ===============================
# CITIES
# ===============================

city_keywords = [

    "Bangalore jobs",

    "Hyderabad jobs",

    "Pune jobs",

    "Delhi jobs",

    "Noida jobs",

    "Gurgaon jobs",

    "Mumbai jobs",

    "Chennai jobs",

    "Ahmedabad jobs",

    "Kolkata jobs"

]


# ===============================
# FRESHERS
# ===============================

fresher_keywords = [

    "fresher jobs india",

    "entry level software engineer",

    "graduate hiring",

    "campus hiring",

    "2026 batch hiring",

    "off campus hiring",

    "new graduate jobs",

    "junior software engineer",

    "associate software engineer",

    "entry level developer"

]


# ===============================
# REMOTE
# ===============================

remote_keywords = [

    "remote software engineer",

    "remote developer india",

    "work from home developer",

    "remote AI engineer",

    "remote internship",

    "remote python developer",

    "remote backend engineer",

    "remote frontend engineer",

    "remote data analyst",

    "remote machine learning"

]


# ===============================
# FINAL KEYWORDS
# ===============================
import random

keywords = (
    software_keywords +
    data_keywords +
    internship_keywords +
    hiring_keywords +
    company_keywords +
    city_keywords +
    fresher_keywords +
    remote_keywords
)

# Remove duplicates
keywords = list(dict.fromkeys(keywords))

# Shuffle in a reproducible way
random.seed(42)
random.shuffle(keywords)