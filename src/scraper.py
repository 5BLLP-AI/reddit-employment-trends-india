from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from urllib.parse import quote

import pandas as pd
import time
import random
import logging

from keywords import keywords


# =====================================================
# Logging
# =====================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)


# =====================================================
# Batch Configuration
# =====================================================

BATCH_SIZE = 20

batch_number = 1       # Change this to 2,3,4... for next batches


start = (batch_number - 1) * BATCH_SIZE
end = start + BATCH_SIZE

keywords = keywords[start:end]

print("=" * 50)
print(f"Running Batch : {batch_number}")
print(f"Keywords      : {len(keywords)}")
print("=" * 50)


# =====================================================
# Chrome Driver
# =====================================================

driver = webdriver.Chrome(
    service=Service(
        ChromeDriverManager().install()
    )
)


data = []


try:

    total_keywords = len(keywords)

    for index, keyword in enumerate(keywords, start=1):

        logging.info(
            f"[{index}/{total_keywords}] Searching : {keyword}"
        )

        url = (
            "https://old.reddit.com/search/?q="
            + quote(keyword)
        )

        driver.get(url)

        # Human-like delay
        time.sleep(
            random.randint(10, 20)
        )

        max_attempts = 3

        posts = []

        for attempt in range(max_attempts):

            page_source = driver.page_source.lower()

            # Detect Block Page
            if "you've been blocked" in page_source:

                logging.warning(
                    "Blocked detected. Refreshing..."
                )

                driver.refresh()

                time.sleep(
                    random.randint(8, 12)
                )

            posts = driver.find_elements(
                By.CSS_SELECTOR,
                "div.search-result"
            )

            if len(posts) > 0:
                break

        logging.info(
            f"{keyword} -> {len(posts)} posts"
        )

        if len(posts) == 0:

            logging.warning(
                f"No posts found for '{keyword}'"
            )

            continue

        for post in posts:

            try:

                title = post.find_element(
                    By.CSS_SELECTOR,
                    "a.search-title"
                ).text

                if not title:
                    continue

                subreddit = post.find_element(
                    By.CSS_SELECTOR,
                    "a.search-subreddit-link"
                ).text

                timestamp = post.find_element(
                    By.CSS_SELECTOR,
                    "time"
                ).get_attribute(
                    "datetime"
                )

                post_url = post.find_element(
                    By.CSS_SELECTOR,
                    "a.search-title"
                ).get_attribute(
                    "href"
                )

                data.append({

                    "keyword": keyword,

                    "title": title,

                    "subreddit": subreddit,

                    "timestamp": timestamp,

                    "post_url": post_url

                })

            except Exception:
                continue


finally:

    driver.quit()


# =====================================================
# Save Batch CSV
# =====================================================

# ==========================================
# Convert list to DataFrame
# ==========================================

df_new = pd.DataFrame(data)

print(f"New Posts Collected : {len(df_new)}")

# ==========================================
# Metadata Columns
# ==========================================

from datetime import datetime

df_new["scrape_date"] = datetime.now().strftime("%Y-%m-%d")

df_new["batch_number"] = batch_number

df_new["source"] = "reddit"

# ==========================================
# Save Individual Batch
# ==========================================

batch_file = (
    f"data/raw/reddit_posts_batch_{batch_number}.csv"
)

df_new.to_csv(
    batch_file,
    index=False
)

print(f"Batch Saved : {batch_file}")

# ==========================================
# Create / Update Master Dataset
# ==========================================

master_file = "data/raw/reddit_posts.csv"

import os

if os.path.exists(master_file):

    print("Existing dataset found...")

    df_old = pd.read_csv(master_file)

    df_master = pd.concat(
        [df_old, df_new],
        ignore_index=True
    )

else:

    print("Creating new master dataset...")

    df_master = df_new

# ==========================================
# Remove Duplicate Posts
# ==========================================

before = len(df_master)

df_master.drop_duplicates(
    subset="post_url",
    inplace=True
)

after = len(df_master)

print(f"Duplicates Removed : {before-after}")

# ==========================================
# Save Master Dataset
# ==========================================

df_master.to_csv(
    master_file,
    index=False
)

print()

print("="*50)

print("MASTER DATASET UPDATED")

print("="*50)

print(f"Total Posts : {len(df_master)}")

print(f"Saved To : {master_file}")

print("="*50)