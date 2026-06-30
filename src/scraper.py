from selenium import webdriver

from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By

from urllib.parse import quote

import pandas as pd

import time
import logging
import random


driver = webdriver.Chrome(

    service=Service(

        ChromeDriverManager().install()

    )

)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)


keywords = [

    "developersindia internship",

    "developersindia hiring",

    "developersindia layoffs",

    "software engineer bangalore",

    "data analyst hyderabad",

    "AI jobs india",

    "fresher jobs india",

    "ML engineer india",

    "hiring india"

]


data = []


for keyword in keywords:

    url = (

        f"https://old.reddit.com"

        f"/search/?q={quote(keyword)}"

    )

    driver.get(url)

    time.sleep(

        random.randint(5, 8)

    )

    max_attempts = 3

    posts = []

    for attempt in range(

        max_attempts

    ):

        page_source = (

            driver.page_source

            .lower()

        )

        if (

            "you've been blocked"

            in page_source

        ):

            print(

                f"{keyword}: blocked"

            )

            driver.refresh()

            time.sleep(5)

        posts = driver.find_elements(

            By.CSS_SELECTOR,

            "div.search-result"

        )

        if len(posts) > 0:

            break

    logging.info(
    f"{keyword} -> {len(posts)} posts"
    )

    for post in posts:

        try:

            title = post.find_element(

                By.CSS_SELECTOR,

                "a.search-title"

            ).text

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


driver.quit()


df = pd.DataFrame(data)

df.to_csv(

    "data/raw/reddit_posts.csv",

    index=False

)

print(

    f"Collected {len(df)} posts"

)