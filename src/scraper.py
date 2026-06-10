from typing import Iterable


def fetch_submissions(reddit, subreddit: str, limit: int = 100) -> Iterable:
    """Yield submissions from a subreddit. Placeholder implementation."""
    sub = reddit.subreddit(subreddit)
    for submission in sub.new(limit=limit):
        yield {
            "id": submission.id,
            "title": submission.title,
            "selftext": submission.selftext,
            "created_utc": submission.created_utc,
        }
