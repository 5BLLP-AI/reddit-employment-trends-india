from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA = PROJECT_ROOT / "data" / "raw" / "reddit_posts.csv"

PROCESSED_DATA = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "reddit_posts_cleaned.csv"
)

REPORT_FILE = (
    PROJECT_ROOT
    / "reports"
    / "data_quality_report.txt"
)