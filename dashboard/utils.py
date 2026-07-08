from __future__ import annotations

import ast
import math
import re
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


APP_TITLE = "Reddit Employment Trends in India"
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data" / "processed"
DEFAULT_DATA_PATH = DATA_DIR / "reddit_posts_final.csv"
REQUIRED_COLUMNS = {
    "title",
    "clean_title",
    "subreddit",
    "timestamp",
    "post_url",
    "keyword",
    "role",
    "skill",
    "location",
}

px.defaults.template = "plotly_dark"
px.defaults.color_discrete_sequence = ["#7DD3FC", "#A78BFA", "#34D399", "#FBBF24", "#F472B6", "#60A5FA", "#F97316", "#22C55E"]

THEME = {
    "bg": "#0B1220",
    "panel": "#111A2E",
    "panel_2": "#162033",
    "panel_3": "#1B2740",
    "border": "rgba(148, 163, 184, 0.16)",
    "text": "#E5EEF8",
    "muted": "#94A3B8",
    "accent": "#7DD3FC",
    "accent_2": "#A78BFA",
}

SKILL_CATEGORY_MAP = {
    "Programming Languages": ["python", "java", "javascript", "typescript", "sql", "c++", "c#", "go", "golang", "php", "ruby", "swift"],
    "Data & Analytics": ["data science", "data analyst", "analytics", "power bi", "tableau", "excel", "statistics", "business intelligence"],
    "AI / ML": ["machine learning", "artificial intelligence", "ai", "ml", "llm", "gpt", "deep learning"],
    "Cloud / DevOps": ["cloud", "devops", "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "jenkins", "ansible"],
    "Backend / APIs": ["backend", "django", "flask", "fastapi", "spring", "node", "api", "microservices"],
    "Frontend / Web": ["frontend", "react", "angular", "vue", "html", "css", "javascript", "nextjs", "next.js"],
    "Tools / Collaboration": ["git", "github", "gitlab", "linux", "jira", "confluence", "postman"],
    "Mobile / Platform": ["android", "ios", "flutter", "react native"],
}

TOPIC_PATTERNS = [
    ("Hiring & Open Roles", ["hiring", "opening", "job", "vacancy", "recruit", "apply", "opportunity"]),
    ("Internships & Entry Level", ["intern", "internship", "fresher", "entry level", "graduate", "campus"]),
    ("Software Engineering", ["software engineer", "developer", "full stack", "frontend", "backend", "web"]),
    ("Data & Analytics", ["data scientist", "data analyst", "analytics", "bi", "sql", "dashboard"]),
    ("AI / ML", ["machine learning", "artificial intelligence", "ai", "llm", "ml engineer", "model"]),
    ("Cloud / DevOps", ["cloud", "devops", "aws", "azure", "docker", "kubernetes", "terraform"]),
    ("Salary / Compensation", ["salary", "ctc", "compensation", "pay", "package", "hike"]),
    ("Interview / Resume", ["interview", "resume", "cv", "portfolio", "oa", "assessment"]),
    ("Career Advice", ["advice", "career", "roadmap", "guide", "suggest", "help"]),
    ("Remote / Location", ["remote", "wfh", "work from home", "bangalore", "hyderabad", "pune", "mumbai", "delhi", "noida", "gurgaon"]),
]

COMPANY_PATTERNS = {
    "Google": [r"\bgoogle\b", r"alphabet"],
    "Microsoft": [r"\bmicrosoft\b"],
    "Amazon": [r"\bamazon\b", r"\baws\b"],
    "Meta": [r"\bmeta\b", r"\bfacebook\b"],
    "Apple": [r"\bapple\b"],
    "Adobe": [r"\badobe\b"],
    "Oracle": [r"\boracle\b"],
    "IBM": [r"\bibm\b"],
    "Intel": [r"\bintel\b"],
    "NVIDIA": [r"\bnvidia\b"],
    "Cisco": [r"\bcisco\b"],
    "SAP": [r"\bsap\b"],
    "Salesforce": [r"\bsalesforce\b"],
    "ServiceNow": [r"\bservicenow\b"],
    "Uber": [r"\buber\b"],
    "Airbnb": [r"\bairbnb\b"],
    "PayPal": [r"\bpaypal\b"],
    "JPMorgan": [r"\bjpmorgan\b", r"\bj\.p\.\s*morgan\b"],
    "Goldman Sachs": [r"\bgoldman sachs\b"],
    "Morgan Stanley": [r"\bmorgan stanley\b"],
    "Deloitte": [r"\bdeloitte\b"],
    "EY": [r"\bey\b", r"ernst & young"],
    "KPMG": [r"\bkpmg\b"],
    "PwC": [r"\bpwc\b"],
    "Accenture": [r"\baccenture\b"],
    "Capgemini": [r"\bcapgemini\b"],
    "Cognizant": [r"\bcognizant\b"],
    "Infosys": [r"\binfosys\b"],
    "TCS": [r"\btcs\b", r"tata consultancy services"],
    "Wipro": [r"\bwipro\b"],
    "HCL": [r"\bhcl\b"],
    "Tech Mahindra": [r"\btech mahindra\b"],
    "LTIMindtree": [r"\bltimindtree\b", r"\blti mindtree\b", r"\bmindtree\b"],
    "Zoho": [r"\bzoho\b"],
    "Freshworks": [r"\bfreshworks\b"],
    "Flipkart": [r"\bflipkart\b"],
    "Paytm": [r"\bpaytm\b"],
    "PhonePe": [r"\bphonepe\b"],
    "Swiggy": [r"\bswiggy\b"],
    "Zomato": [r"\bzomato\b"],
    "CRED": [r"\bcred\b"],
    "Razorpay": [r"\brazorpay\b"],
    "InMobi": [r"\binmobi\b"],
    "Ola": [r"\bola\b"],
    "Airtel": [r"\baitel\b"],
    "Reliance": [r"\breliance\b"],
    "Walmart": [r"\bwalmart\b"],
    "Target": [r"\btarget\b"],
    "Turing": [r"\bturing\b"],
    "OpenAI": [r"\bopenai\b"],
}

CITY_TO_STATE = {
    "Bangalore": "Karnataka",
    "Bengaluru": "Karnataka",
    "Hyderabad": "Telangana",
    "Pune": "Maharashtra",
    "Mumbai": "Maharashtra",
    "Delhi": "Delhi",
    "New Delhi": "Delhi",
    "Noida": "Uttar Pradesh",
    "Gurgaon": "Haryana",
    "Gurugram": "Haryana",
    "Chennai": "Tamil Nadu",
    "Kolkata": "West Bengal",
    "Ahmedabad": "Gujarat",
    "Remote": "Remote",
}

POSITIVE_WORDS = {"hired", "hiring", "offer", "offers", "selected", "success", "growth", "opportunity", "exciting", "approved", "promoted", "salary hike", "bonus"}
NEGATIVE_WORDS = {"rejected", "reject", "layoff", "layoffs", "fired", "scam", "ghosted", "toxic", "problem", "issue", "low", "declined", "delay", "uncertain", "burnout"}


def _strip_unknown(value: object) -> str:
    if isinstance(value, (list, tuple, set, np.ndarray)):
        cleaned_items = [str(item).strip() for item in value if str(item).strip()]
        return ", ".join(cleaned_items) if cleaned_items else "Unknown"
    try:
        if pd.isna(value):
            return "Unknown"
    except (TypeError, ValueError):
        pass
    text = str(value).strip()
    if not text or text.lower() in {"nan", "none", "null", "unknown"}:
        return "Unknown"
    return text


def _clean_text(text: object) -> str:
    return _strip_unknown(text).lower()


def _ensure_datetime(series: pd.Series) -> pd.Series:
    parsed = pd.to_datetime(series, errors="coerce", utc=True)
    if hasattr(parsed, "dt"):
        return parsed.dt.tz_convert(None)
    return parsed


def _split_multi_value(value: object) -> list[str]:
    if isinstance(value, (list, tuple, set)):
        return [str(item).strip() for item in value if str(item).strip() and str(item).lower() != "unknown"]
    if isinstance(value, np.ndarray):
        return [str(item).strip() for item in value.tolist() if str(item).strip() and str(item).lower() != "unknown"]
    text = _strip_unknown(value)
    if text == "Unknown":
        return []
    if text.startswith("[") and text.endswith("]"):
        try:
            parsed = ast.literal_eval(text)
            if isinstance(parsed, (list, tuple, set)):
                return [str(item).strip() for item in parsed if str(item).strip() and str(item).lower() != "unknown"]
        except (ValueError, SyntaxError):
            pass
    parts = [part.strip() for part in re.split(r"[,|;/]", text) if part.strip()]
    return [part for part in parts if part.lower() != "unknown"]


def _unique_nonempty(values: Iterable[object]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        text = _strip_unknown(value)
        if text == "Unknown" or text in seen:
            continue
        seen.add(text)
        ordered.append(text)
    return ordered


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns={column: column.strip() for column in df.columns}).copy()
    for column in ["title", "clean_title", "subreddit", "skill", "role", "location", "keyword", "scrape_date", "post_url", "source", "sentiment", "topic", "cluster", "score"]:
        if column in df.columns:
            df[column] = df[column].apply(_strip_unknown)
    return df


def _merge_optional_column(base: pd.DataFrame, path: Path, columns: Sequence[str], rename_map: dict[str, str] | None = None) -> pd.DataFrame:
    if not path.exists():
        return base
    aux = _normalize_columns(pd.read_csv(path)).rename(columns=rename_map or {})
    merge_columns = ["post_url"] + [column for column in columns if column in aux.columns]
    if len(merge_columns) <= 1:
        return base
    aux = aux[merge_columns].drop_duplicates(subset=["post_url"], keep="first")
    merged = base.merge(aux, on="post_url", how="left", suffixes=("", "_aux"))
    for column in columns:
        aux_column = f"{column}_aux"
        if column not in merged.columns and aux_column in merged.columns:
            merged[column] = merged[aux_column]
        elif column in merged.columns and aux_column in merged.columns:
            merged[column] = merged[column].where(merged[column].notna(), merged[aux_column])
        if aux_column in merged.columns:
            merged = merged.drop(columns=[aux_column])
    return merged


def _parse_company_mentions(text: object) -> list[str]:
    content = _clean_text(text)
    if content == "unknown":
        return []
    found: list[str] = []
    for company, patterns in COMPANY_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, content, flags=re.IGNORECASE):
                found.append(company)
                break
    return _unique_nonempty(found)


def _parse_topic_label(text: object, role: object = None, skill: object = None, location: object = None) -> str:
    content = " ".join([_clean_text(text), _clean_text(role), _clean_text(skill), _clean_text(location)])
    for label, terms in TOPIC_PATTERNS:
        if any(term in content for term in terms):
            return label
    return "Other"


def _parse_sentiment(text: object) -> tuple[str, float]:
    content = _clean_text(text)
    if content == "unknown":
        return "Neutral", 0.0
    positive_hits = sum(1 for word in POSITIVE_WORDS if word in content)
    negative_hits = sum(1 for word in NEGATIVE_WORDS if word in content)
    score = float(positive_hits - negative_hits)
    if score > 0:
        return "Positive", min(score / 3.0, 1.0)
    if score < 0:
        return "Negative", max(score / 3.0, -1.0)
    return "Neutral", 0.0


def _primary_value(value: object) -> str:
    values = _split_multi_value(value)
    return values[0] if values else _strip_unknown(value)


def _state_from_location(value: object) -> str:
    items = _split_multi_value(value)
    states: list[str] = []
    for item in items:
        state = CITY_TO_STATE.get(item)
        if state and state not in states:
            states.append(state)
    if states:
        return ", ".join(states)
    return _strip_unknown(value)


def _skill_category(skill: object) -> str:
    text = _clean_text(skill)
    if text == "unknown":
        return "Unknown"
    for category, keywords in SKILL_CATEGORY_MAP.items():
        if any(keyword in text for keyword in keywords):
            return category
    return "Other"


@st.cache_data(show_spinner=False)
def load_dashboard_data() -> pd.DataFrame:
    if not DEFAULT_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Missing dataset: {DEFAULT_DATA_PATH}. Rebuild the processed CSV before launching the dashboard."
        )

    df = _normalize_columns(pd.read_csv(DEFAULT_DATA_PATH))
    missing_columns = sorted(REQUIRED_COLUMNS - set(df.columns))
    if missing_columns:
        raise ValueError(
            "The dashboard dataset is missing required columns: "
            + ", ".join(missing_columns)
            + "."
        )

    if "post_url" not in df.columns:
        df["post_url"] = np.arange(len(df)).astype(str)

    df = _merge_optional_column(df, DATA_DIR / "reddit_posts_sentiment.csv", ["sentiment", "score"], {"score": "sentiment_score"})
    df = _merge_optional_column(df, DATA_DIR / "reddit_posts_topics.csv", ["topic"])
    df = _merge_optional_column(df, DATA_DIR / "reddit_posts_clustered.csv", ["cluster"])

    if "sentiment" not in df.columns:
        sentiment_result = df["clean_title"].apply(_parse_sentiment)
        df["sentiment"] = sentiment_result.apply(lambda value: value[0])
        df["sentiment_score"] = sentiment_result.apply(lambda value: value[1])
    else:
        sentiment_result = df["clean_title"].apply(_parse_sentiment)
        if "sentiment_score" not in df.columns:
            df["sentiment_score"] = sentiment_result.apply(lambda value: value[1])
        df["sentiment"] = df["sentiment"].apply(lambda value: _strip_unknown(value) if _strip_unknown(value) != "Unknown" else np.nan).fillna(sentiment_result.apply(lambda value: value[0]))

    df["timestamp"] = _ensure_datetime(df.get("timestamp", pd.Series([pd.NaT] * len(df))))
    df["scrape_date"] = pd.to_datetime(df.get("scrape_date", pd.Series([pd.NaT] * len(df))), errors="coerce", utc=True, format="mixed")
    df["date"] = df["timestamp"].dt.date
    df["year"] = df["timestamp"].dt.year
    df["month"] = df["timestamp"].dt.to_period("M").astype(str)
    df["week"] = df["timestamp"].dt.to_period("W").astype(str)
    df["month_start"] = df["timestamp"].dt.to_period("M").dt.to_timestamp()
    df["week_start"] = df["timestamp"].dt.to_period("W").dt.start_time

    df["skill"] = df["skill"].apply(_strip_unknown) if "skill" in df.columns else "Unknown"
    df["location"] = df["location"].apply(_strip_unknown) if "location" in df.columns else "Unknown"
    df["role"] = df["role"].apply(_strip_unknown) if "role" in df.columns else "Unknown"
    if "keyword" not in df.columns:
        df["keyword"] = "Unknown"

    title_frame = df[[column for column in ["title", "clean_title", "keyword"] if column in df.columns]].fillna("")
    df["company_list"] = title_frame.agg(" ".join, axis=1).apply(_parse_company_mentions)
    df["company"] = df["company_list"].apply(lambda items: ", ".join(items) if items else "Unknown")
    df["company_primary"] = df["company_list"].apply(lambda items: items[0] if items else "Unknown")

    df["topic_label"] = df[["clean_title", "role", "skill", "location"]].apply(lambda row: _parse_topic_label(row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3]), axis=1)
    df["skill_category"] = df["skill"].apply(_skill_category)
    df["location_state"] = df["location"].apply(_state_from_location)
    df["role_primary"] = df["role"].apply(_primary_value)
    df["skill_primary"] = df["skill"].apply(_primary_value)
    df["location_primary"] = df["location"].apply(_primary_value)

    if "cluster" in df.columns:
        df["cluster"] = pd.to_numeric(df["cluster"], errors="coerce").fillna(-1).astype(int)
    else:
        df["cluster"] = -1

    if "topic" in df.columns:
        df["topic"] = pd.to_numeric(df["topic"], errors="coerce").fillna(-1).astype(int)
    else:
        df["topic"] = -1

    df["topic_display"] = np.where(df["topic"] >= 0, df["topic"].map(lambda value: f"Topic {int(value) + 1}"), df["topic_label"])
    df["search_blob"] = df[[column for column in ["title", "clean_title", "keyword", "role", "skill", "location", "company", "subreddit", "sentiment", "topic_display"] if column in df.columns]].fillna("").agg(" ".join, axis=1)
    return df


def inject_dashboard_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg: #0B1220;
            --panel: #111A2E;
            --panel-2: #162033;
            --panel-3: #1B2740;
            --border: rgba(148, 163, 184, 0.18);
            --text: #E5EEF8;
            --muted: #94A3B8;
            --accent: #7DD3FC;
            --accent-2: #A78BFA;
        }
        html, body, [class*="css"] { font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif; }
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(125, 211, 252, 0.12), transparent 28%),
                radial-gradient(circle at top right, rgba(167, 139, 250, 0.10), transparent 24%),
                linear-gradient(180deg, #0B1220 0%, #0B1220 100%);
            color: var(--text);
        }
        .block-container {
            padding-top: 7rem;
            padding-bottom: 2rem;
            max-width: 1600px;
        }
        header[data-testid="stHeader"] {
            display: none;
        }
        div[data-testid="stToolbar"] {
            display: none;
        }
        section[data-testid="stSidebar"] { background: linear-gradient(180deg, rgba(17, 26, 46, 0.98), rgba(11, 18, 32, 0.98)); border-right: 1px solid var(--border); }
        .dashboard-title { font-size: 2.2rem; font-weight: 800; letter-spacing: -0.04em; line-height: 1.08; margin: 0.35rem 0 0.35rem 0; padding-top: 0.25rem; }
        .dashboard-subtitle { color: var(--muted); font-size: 0.98rem; max-width: 75rem; margin-bottom: 1.1rem; }
        .section-title { font-size: 1.15rem; font-weight: 700; margin: 0.2rem 0 0.8rem 0; color: var(--text); }
        .metric-card { background: linear-gradient(180deg, rgba(22, 32, 51, 0.95), rgba(17, 26, 46, 0.95)); border: 1px solid var(--border); border-radius: 20px; padding: 1rem 1rem 0.95rem 1rem; box-shadow: 0 12px 30px rgba(0, 0, 0, 0.18); }
        .metric-label { color: var(--muted); font-size: 0.78rem; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 0.5rem; }
        .metric-value { font-size: 1.9rem; font-weight: 800; line-height: 1.0; color: var(--text); }
        .metric-caption { color: var(--muted); font-size: 0.83rem; margin-top: 0.45rem; }
        .panel-card { background: linear-gradient(180deg, rgba(22, 32, 51, 0.94), rgba(17, 26, 46, 0.94)); border: 1px solid var(--border); border-radius: 20px; padding: 1rem 1rem 0.75rem 1rem; box-shadow: 0 12px 30px rgba(0, 0, 0, 0.16); }
        .pipeline { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 0.75rem; }
        .pipeline-step { background: rgba(27, 39, 64, 0.85); border: 1px solid var(--border); border-radius: 16px; padding: 0.9rem; text-align: center; min-height: 94px; }
        .pipeline-step strong { display: block; font-size: 0.95rem; margin-bottom: 0.35rem; }
        .pipeline-step span { color: var(--muted); font-size: 0.83rem; line-height: 1.4; }
        .dataset-summary { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0.8rem; }
        .summary-item { background: rgba(27, 39, 64, 0.72); border: 1px solid var(--border); border-radius: 16px; padding: 0.9rem; }
        .summary-item .label { color: var(--muted); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.06em; }
        .summary-item .value { font-size: 1.35rem; font-weight: 800; margin-top: 0.2rem; }
        .summary-item .note { color: var(--muted); font-size: 0.82rem; margin-top: 0.2rem; }
        .stButton button, .stDownloadButton button { border-radius: 12px; border: 1px solid rgba(125, 211, 252, 0.2); background: linear-gradient(180deg, rgba(37, 99, 235, 0.95), rgba(29, 78, 216, 0.95)); color: white; font-weight: 600; }
        .stButton button:hover, .stDownloadButton button:hover { border-color: rgba(125, 211, 252, 0.4); transform: translateY(-1px); }
        .filter-summary { background: rgba(22, 32, 51, 0.75); border: 1px solid var(--border); border-radius: 16px; padding: 0.75rem 0.9rem; color: var(--muted); }
        @media (max-width: 1100px) { .block-container { padding-top: 6rem; } .pipeline, .dataset-summary { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
        @media (max-width: 700px) { .block-container { padding-top: 5.5rem; } .pipeline, .dataset-summary { grid-template-columns: repeat(1, minmax(0, 1fr)); } }
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_header(title: str, subtitle: str) -> None:
    st.markdown(f'<div class="dashboard-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="dashboard-subtitle">{subtitle}</div>', unsafe_allow_html=True)


def render_metric_cards(metrics: Sequence[dict[str, str]]) -> None:
    rows = [metrics[index : index + 4] for index in range(0, len(metrics), 4)]
    for row in rows:
        columns = st.columns(4)
        for column, metric in zip(columns, row):
            with column:
                st.markdown(f"<div class='metric-card'><div class='metric-label'>{metric['label']}</div><div class='metric-value'>{metric['value']}</div><div class='metric-caption'>{metric.get('caption', '')}</div></div>", unsafe_allow_html=True)


def render_pipeline_diagram() -> None:
    st.markdown('<div class="section-title">Pipeline View</div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="panel-card">
            <div class="pipeline">
                <div class="pipeline-step"><strong>Collection</strong><span>Reddit posts collected from employment-related communities and normalized into a single curated dataset.</span></div>
                <div class="pipeline-step"><strong>Enrichment</strong><span>Skills, roles, locations, companies, sentiment, and topics are standardized and enriched for analytics.</span></div>
                <div class="pipeline-step"><strong>Modeling</strong><span>Trend, clustering, and topic views provide structured signals for operational decision-making.</span></div>
                <div class="pipeline-step"><strong>Dashboard</strong><span>Interactive filters, searchable tables, and executive summaries support fast exploration.</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_dataset_summary(df: pd.DataFrame) -> None:
    latest_scrape = df["scrape_date"].dropna().max()
    latest_scrape_text = pd.Timestamp(latest_scrape).strftime("%Y-%m-%d") if pd.notna(latest_scrape) else "Unknown"
    date_span = "Unknown"
    if df["timestamp"].notna().any():
        date_span = f"{df['timestamp'].min().date()} to {df['timestamp'].max().date()}"
    summary = [
        ("Data source", DEFAULT_DATA_PATH.name, "Primary curated dataset"),
        ("Rows", f"{len(df):,}", "Posts currently available"),
        ("Date span", date_span, "Coverage in the current file"),
        ("Latest scrape", latest_scrape_text, "Most recent ingestion date"),
    ]
    st.markdown('<div class="section-title">Dataset Summary</div>', unsafe_allow_html=True)
    st.markdown("<div class='dataset-summary'>" + "".join(f"<div class='summary-item'><div class='label'>{label}</div><div class='value'>{value}</div><div class='note'>{note}</div></div>" for label, value, note in summary) + "</div>", unsafe_allow_html=True)


def render_filter_summary(filtered_df: pd.DataFrame, total_df: pd.DataFrame) -> None:
    total = len(total_df)
    filtered = len(filtered_df)
    pct = 0 if total == 0 else round(filtered / total * 100, 1)
    st.markdown(f"<div class='filter-summary'>Showing <strong>{filtered:,}</strong> of <strong>{total:,}</strong> posts ({pct}%). Use the sidebar filters to narrow the analysis.</div>", unsafe_allow_html=True)


def _sorted_options(series: pd.Series) -> list[str]:
    return sorted(_unique_nonempty(series.dropna().astype(str).tolist()))


def _filter_multi_value(df: pd.DataFrame, column: str, selected: Sequence[str]) -> pd.DataFrame:
    if not selected or column not in df.columns:
        return df
    selected_set = {str(item).strip() for item in selected if str(item).strip()}
    if not selected_set:
        return df

    def matches(value: object) -> bool:
        values = _split_multi_value(value)
        if not values:
            return _strip_unknown(value) == "Unknown" and "Unknown" in selected_set
        return any(item in selected_set for item in values) or (_strip_unknown(value) in selected_set)

    return df[df[column].apply(matches)]


def apply_sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.markdown("### Global Filters")
    st.sidebar.caption("These filters persist across dashboard pages.")

    skill_series = pd.Series([item for row in df["skill"].apply(_split_multi_value) for item in row])
    location_series = pd.Series([item for row in df["location"].apply(_split_multi_value) for item in row])
    company_series = pd.Series([item for row in df["company_list"].apply(lambda items: items if isinstance(items, list) else []) for item in row])

    role_options = _sorted_options(df["role"])
    skill_options = _sorted_options(skill_series) if not skill_series.empty else []
    location_options = _sorted_options(location_series) if not location_series.empty else []
    company_options = _sorted_options(company_series) if not company_series.empty else []
    sentiment_options = _sorted_options(df["sentiment"])
    topic_options = _sorted_options(df["topic_display"])
    subreddit_options = _sorted_options(df["subreddit"])

    selected_roles = st.sidebar.multiselect("Role", role_options, default=role_options, key="filter_role")
    selected_skills = st.sidebar.multiselect("Skill", skill_options, default=skill_options, key="filter_skill")
    selected_locations = st.sidebar.multiselect("Location", location_options, default=location_options, key="filter_location")
    selected_companies = st.sidebar.multiselect("Company", company_options, default=company_options, key="filter_company")
    selected_sentiments = st.sidebar.multiselect("Sentiment", sentiment_options, default=sentiment_options, key="filter_sentiment")
    selected_topics = st.sidebar.multiselect("Topic", topic_options, default=topic_options, key="filter_topic")
    selected_subreddits = st.sidebar.multiselect("Subreddit", subreddit_options, default=subreddit_options, key="filter_subreddit")

    available_dates = df["timestamp"].dropna()
    if available_dates.empty:
        min_date = max_date = pd.Timestamp.today().date()
    else:
        min_date = available_dates.min().date()
        max_date = available_dates.max().date()

    selected_date_range = st.sidebar.date_input("Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date, key="filter_date_range")

    filtered = df.copy()
    filtered = filtered[filtered["role"].isin(selected_roles)] if selected_roles else filtered.iloc[0:0]
    filtered = _filter_multi_value(filtered, "skill", selected_skills)
    filtered = _filter_multi_value(filtered, "location", selected_locations)
    filtered = _filter_multi_value(filtered, "company_list", selected_companies)
    filtered = filtered[filtered["sentiment"].isin(selected_sentiments)] if selected_sentiments else filtered.iloc[0:0]
    filtered = filtered[filtered["topic_display"].isin(selected_topics)] if selected_topics else filtered.iloc[0:0]
    filtered = filtered[filtered["subreddit"].isin(selected_subreddits)] if selected_subreddits else filtered.iloc[0:0]

    if isinstance(selected_date_range, tuple) and len(selected_date_range) == 2:
        start_date, end_date = selected_date_range
    else:
        start_date = end_date = selected_date_range
    filtered = filtered[(filtered["timestamp"].dt.date >= start_date) & (filtered["timestamp"].dt.date <= end_date)]

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Active rows:** {len(filtered):,}")
    return filtered


def explode_values(df: pd.DataFrame, column: str, value_name: str | None = None) -> pd.DataFrame:
    value_name = value_name or column
    if column not in df.columns:
        return pd.DataFrame(columns=[value_name])
    exploded = df[[column]].copy()
    exploded[column] = exploded[column].apply(_split_multi_value)
    exploded = exploded.explode(column)
    exploded[column] = exploded[column].apply(_strip_unknown)
    exploded = exploded[exploded[column] != "Unknown"]
    return exploded.rename(columns={column: value_name})


def count_multi_value(df: pd.DataFrame, column: str, top_n: int = 10) -> pd.DataFrame:
    exploded = explode_values(df, column, value_name=column)
    if exploded.empty:
        return pd.DataFrame({column: [], "count": []})
    counts = exploded.value_counts().reset_index(name="count")
    counts.columns = [column, "count"]
    return counts.head(top_n)


def unique_multi_value_count(df: pd.DataFrame, column: str) -> int:
    exploded = explode_values(df, column, value_name=column)
    if exploded.empty:
        return 0
    return int(exploded[column].nunique())


def make_bar_chart(df: pd.DataFrame, x: str, y: str, title: str, orientation: str = "v", color: str | None = None, height: int = 420):
    fig = px.bar(df, x=x, y=y, color=color or y, orientation=orientation, title=title)
    fig.update_layout(height=height, margin=dict(l=10, r=10, t=60, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color=THEME["text"]), legend_title_text="")
    if orientation == "h":
        fig.update_yaxes(autorange="reversed")
    return fig


def make_line_chart(df: pd.DataFrame, x: str, y: str, title: str, color: str | None = None, height: int = 420):
    fig = px.line(df, x=x, y=y, color=color, markers=True, title=title)
    fig.update_layout(height=height, margin=dict(l=10, r=10, t=60, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color=THEME["text"]), legend_title_text="")
    return fig


def make_pie_chart(df: pd.DataFrame, names: str, values: str, title: str, height: int = 420):
    fig = px.pie(df, names=names, values=values, title=title, hole=0.35)
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(height=height, margin=dict(l=10, r=10, t=60, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color=THEME["text"]))
    return fig


def make_treemap(df: pd.DataFrame, path: Sequence[str], values: str, title: str, height: int = 520):
    fig = px.treemap(df, path=list(path), values=values, title=title)
    fig.update_layout(height=height, margin=dict(l=10, r=10, t=60, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color=THEME["text"]))
    return fig


def make_sunburst(df: pd.DataFrame, path: Sequence[str], values: str, title: str, height: int = 520):
    fig = px.sunburst(df, path=list(path), values=values, title=title)
    fig.update_layout(height=height, margin=dict(l=10, r=10, t=60, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color=THEME["text"]))
    return fig


def make_heatmap(data: pd.DataFrame, x: str, y: str, z: str, title: str, height: int = 520):
    pivot = data.pivot_table(index=y, columns=x, values=z, aggfunc="sum", fill_value=0)
    if pivot.empty:
        pivot = pd.DataFrame([[0]], index=["No data"], columns=["No data"])
    fig = px.imshow(pivot, text_auto=True, aspect="auto", color_continuous_scale=["#0F172A", "#2563EB", "#7DD3FC"], title=title)
    fig.update_layout(height=height, margin=dict(l=10, r=10, t=60, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color=THEME["text"]), coloraxis_colorbar=dict(title="Count"))
    return fig


def make_histogram(df: pd.DataFrame, x: str, color: str | None, title: str, nbins: int | None = None, height: int = 420):
    fig = px.histogram(df, x=x, color=color, nbins=nbins, title=title)
    fig.update_layout(height=height, margin=dict(l=10, r=10, t=60, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color=THEME["text"]), legend_title_text="")
    return fig


def top_counts(df: pd.DataFrame, column: str, top_n: int = 10) -> pd.DataFrame:
    if column not in df.columns:
        return pd.DataFrame({column: [], "count": []})
    series = df[column].apply(_strip_unknown)
    counts = series[series != "Unknown"].value_counts().head(top_n).reset_index()
    counts.columns = [column, "count"]
    return counts


def make_time_series(df: pd.DataFrame, period: str = "M") -> pd.DataFrame:
    temp = df.dropna(subset=["timestamp"]).copy()
    if temp.empty:
        return pd.DataFrame({"date": [], "count": []})
    if period == "W":
        temp["date"] = temp["timestamp"].dt.to_period("W").dt.start_time
    else:
        temp["date"] = temp["timestamp"].dt.to_period("M").dt.to_timestamp()
    grouped = temp.groupby("date").size().reset_index(name="count")
    return grouped.sort_values("date")


def search_dataframe(df: pd.DataFrame, query: str) -> pd.DataFrame:
    if not query:
        return df
    pattern = re.escape(query.strip())
    mask = df["search_blob"].fillna("").str.contains(pattern, case=False, na=False, regex=True)
    return df[mask]


def render_paginated_table(df: pd.DataFrame, *, table_key: str, columns: Sequence[str] | None = None, title: str = "Table", export_name: str = "filtered_data.csv", search_hint: str = "Search rows", page_size_options: Sequence[int] = (10, 20, 50, 100)) -> pd.DataFrame:
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    search_query = st.text_input(search_hint, key=f"{table_key}_search")
    view = search_dataframe(df, search_query)

    if view.empty:
        st.info("No rows match the current filters and search text.")
        st.download_button("Download CSV", data=view.to_csv(index=False).encode("utf-8"), file_name=export_name, mime="text/csv", key=f"{table_key}_download_empty")
        return view

    display_columns = [column for column in (columns or view.columns.tolist()) if column in view.columns]
    sort_options = display_columns or view.columns.tolist()
    sort_col = st.selectbox("Sort by", sort_options, index=0, key=f"{table_key}_sort_col")
    sort_direction = st.selectbox("Sort order", ["Descending", "Ascending"], index=0, key=f"{table_key}_sort_dir")
    page_size = st.selectbox("Rows per page", list(page_size_options), index=1 if len(page_size_options) > 1 else 0, key=f"{table_key}_page_size")

    if sort_col in view.columns:
        view = view.sort_values(sort_col, ascending=sort_direction == "Ascending", kind="mergesort")

    total_rows = len(view)
    total_pages = max(1, math.ceil(total_rows / page_size))
    page_number = st.number_input("Page", min_value=1, max_value=total_pages, value=1, step=1, key=f"{table_key}_page_number")
    start = int((page_number - 1) * page_size)
    end = int(start + page_size)
    paged = view.iloc[start:end]

    st.caption(f"Showing rows {start + 1:,} to {min(end, total_rows):,} of {total_rows:,}")
    st.dataframe(paged[display_columns], use_container_width=True, hide_index=True)
    st.download_button("Download CSV", data=view.to_csv(index=False).encode("utf-8"), file_name=export_name, mime="text/csv", key=f"{table_key}_download")
    return view


def _role_skill_matrix(df: pd.DataFrame, top_roles: int = 8, top_skills: int = 10) -> pd.DataFrame:
    roles = top_counts(df, "role", top_roles)["role"].tolist()
    skills = count_multi_value(df, "skill", top_skills)["skill"].tolist()
    records: list[dict[str, object]] = []
    for role in roles:
        role_rows = df[df["role"] == role]
        exploded = role_rows[["skill"]].copy()
        exploded["skill"] = exploded["skill"].apply(_split_multi_value)
        exploded = exploded.explode("skill")
        exploded["skill"] = exploded["skill"].apply(_strip_unknown)
        exploded = exploded[exploded["skill"].isin(skills)]
        counts = exploded["skill"].value_counts()
        for skill, count in counts.items():
            records.append({"role": role, "skill": skill, "count": int(count)})
    return pd.DataFrame(records)


def _location_skill_matrix(df: pd.DataFrame, top_locations: int = 8, top_skills: int = 10) -> pd.DataFrame:
    locations = count_multi_value(df, "location", top_locations)["location"].tolist()
    skills = count_multi_value(df, "skill", top_skills)["skill"].tolist()
    records: list[dict[str, object]] = []
    for location in locations:
        location_rows = df[df["location"].apply(lambda value: location in _split_multi_value(value))]
        exploded = location_rows[["skill"]].copy()
        exploded["skill"] = exploded["skill"].apply(_split_multi_value)
        exploded = exploded.explode("skill")
        exploded["skill"] = exploded["skill"].apply(_strip_unknown)
        exploded = exploded[exploded["skill"].isin(skills)]
        counts = exploded["skill"].value_counts()
        for skill, count in counts.items():
            records.append({"location": location, "skill": skill, "count": int(count)})
    return pd.DataFrame(records)


def _role_location_matrix(df: pd.DataFrame, top_roles: int = 8, top_locations: int = 10) -> pd.DataFrame:
    roles = top_counts(df, "role", top_roles)["role"].tolist()
    locations = count_multi_value(df, "location", top_locations)["location"].tolist()
    records: list[dict[str, object]] = []
    for role in roles:
        role_rows = df[df["role"] == role]
        for location in locations:
            count = role_rows["location"].apply(lambda value: location in _split_multi_value(value)).sum()
            records.append({"role": role, "location": location, "count": int(count)})
    return pd.DataFrame(records)


def _topic_keyword_frame(df: pd.DataFrame, top_n: int = 6) -> pd.DataFrame:
    records = []
    for topic_label, group in df.groupby("topic_display"):
        tokens = group["clean_title"].fillna("").str.lower().str.replace(r"[^a-z0-9\s]", " ", regex=True).str.split()
        words = [word for row in tokens for word in row if len(word) > 2]
        common_words = pd.Series(words).value_counts().head(top_n).index.tolist() if words else []
        records.append({"topic_display": topic_label, "count": len(group), "keywords": ", ".join(common_words) if common_words else "Unknown"})
    result = pd.DataFrame(records)
    if not result.empty:
        result = result.sort_values("count", ascending=False)
    return result


def _recent_vs_previous(df: pd.DataFrame, column: str, days: int = 30, top_n: int = 5) -> pd.DataFrame:
    temp = df.dropna(subset=["timestamp"]).copy()
    if temp.empty or column not in temp.columns:
        return pd.DataFrame({column: [], "recent": [], "previous": [], "delta": []})
    end_date = temp["timestamp"].max()
    recent_start = end_date - pd.Timedelta(days=days)
    previous_start = recent_start - pd.Timedelta(days=days)
    recent = temp[temp["timestamp"] >= recent_start]
    previous = temp[(temp["timestamp"] < recent_start) & (temp["timestamp"] >= previous_start)]
    recent_counts = top_counts(recent, column, top_n)
    previous_counts = top_counts(previous, column, top_n)
    merged = recent_counts.merge(previous_counts, on=column, how="outer", suffixes=("_recent", "_previous")).fillna(0)
    merged["recent"] = merged.get("count_recent", merged.get("recent", 0))
    merged["previous"] = merged.get("count_previous", merged.get("previous", 0))
    if "count_recent" in merged.columns:
        merged = merged.drop(columns=["count_recent"])
    if "count_previous" in merged.columns:
        merged = merged.drop(columns=["count_previous"])
    merged["delta"] = merged["recent"] - merged["previous"]
    return merged.sort_values(["delta", "recent"], ascending=False).head(top_n)


def render_overview_page(df: pd.DataFrame, filtered_df: pd.DataFrame | None = None) -> None:
    inject_dashboard_styles()
    page_header(APP_TITLE, "Executive view of hiring demand, skills, roles, companies, sentiment, topics, and time-based hiring trends across Reddit employment communities.")
    filtered = filtered_df if filtered_df is not None else apply_sidebar_filters(df)
    render_filter_summary(filtered, df)

    latest_scrape = df["scrape_date"].dropna().max()
    latest_scrape_text = pd.Timestamp(latest_scrape).strftime("%Y-%m-%d") if pd.notna(latest_scrape) else "Unknown"
    avg_sentiment = filtered["sentiment_score"].dropna().mean() if "sentiment_score" in filtered.columns and filtered["sentiment_score"].notna().any() else 0.0

    metrics = [
        {"label": "Total Posts", "value": f"{len(filtered):,}", "caption": "Rows after global filters"},
        {"label": "Total Roles", "value": f"{filtered['role'].replace('Unknown', pd.NA).dropna().nunique():,}", "caption": "Distinct roles detected"},
        {"label": "Total Skills", "value": f"{unique_multi_value_count(filtered, 'skill'):,}", "caption": "Distinct skill terms"},
        {"label": "Total Locations", "value": f"{unique_multi_value_count(filtered, 'location'):,}", "caption": "Distinct location terms"},
        {"label": "Total Companies Mentioned", "value": f"{unique_multi_value_count(filtered, 'company_list'):,}", "caption": "Unique company mentions"},
        {"label": "Total Subreddits", "value": f"{filtered['subreddit'].replace('Unknown', pd.NA).dropna().nunique():,}", "caption": "Communities represented"},
        {"label": "Average Sentiment", "value": f"{avg_sentiment:.2f}", "caption": "Varying from -1.0 to 1.0"},
        {"label": "Latest Scrape Date", "value": latest_scrape_text, "caption": "Most recent ingestion"},
    ]
    render_metric_cards(metrics)

    st.write("")
    left, right = st.columns([1.1, 0.9])
    with left:
        render_pipeline_diagram()
    with right:
        render_dataset_summary(df)

    st.write("")
    latest_posts = filtered.sort_values("timestamp", ascending=False).head(8)
    top_discussions = filtered.assign(discussion=np.where(filtered["topic_display"] != "Other", filtered["topic_display"], filtered["keyword"]))
    top_discussions = top_discussions.groupby("discussion").size().reset_index(name="count").sort_values("count", ascending=False).head(8)
    trend_companies = _recent_vs_previous(filtered, "company_primary", top_n=5)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="section-title">Recent Posts</div>', unsafe_allow_html=True)
        st.dataframe(latest_posts[["timestamp", "title", "role", "skill", "location", "company", "subreddit"]].rename(columns={"timestamp": "Timestamp", "title": "Title", "role": "Role", "skill": "Skill", "location": "Location", "company": "Company", "subreddit": "Subreddit"}), use_container_width=True, hide_index=True)
        st.download_button("Download Filtered CSV", data=filtered.to_csv(index=False).encode("utf-8"), file_name="reddit_employment_filtered_overview.csv", mime="text/csv", key="overview_download_filtered")
    with col_b:
        st.markdown('<div class="section-title">Top Discussions and Trending Companies</div>', unsafe_allow_html=True)
        if not top_discussions.empty:
            st.plotly_chart(make_bar_chart(top_discussions, x="count", y="discussion", title="Top Discussions", orientation="h", color="count", height=360), use_container_width=True)
        if not trend_companies.empty:
            st.dataframe(trend_companies.rename(columns={"company_primary": "Company", "recent": "Recent", "previous": "Previous", "delta": "Delta"}), use_container_width=True, hide_index=True)

    st.write("")
    skill_trend = _recent_vs_previous(filtered, "skill_primary", top_n=5)
    role_trend = _recent_vs_previous(filtered, "role_primary", top_n=5)
    location_trend = _recent_vs_previous(filtered, "location_primary", top_n=5)
    t1, t2, t3 = st.columns(3)
    for column, frame, title in [(t1, skill_trend, "Trending Skills"), (t2, role_trend, "Trending Roles"), (t3, location_trend, "Trending Locations")]:
        with column:
            st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
            if frame.empty:
                st.info("No trend data available.")
            else:
                display = frame.rename(columns={frame.columns[0]: title.split()[-1], "recent": "Recent", "previous": "Previous", "delta": "Delta"})
                st.dataframe(display, use_container_width=True, hide_index=True)


def render_skills_page(df: pd.DataFrame, filtered_df: pd.DataFrame | None = None) -> None:
    inject_dashboard_styles()
    page_header("Skills and Demand", "Skills extracted from employment discussions, grouped into categories and compared by role, location, sentiment, and company mentions.")
    filtered = filtered_df if filtered_df is not None else apply_sidebar_filters(df)
    render_filter_summary(filtered, df)

    skills = count_multi_value(filtered, "skill", top_n=15)
    categories = filtered.groupby("skill_category").size().reset_index(name="count").sort_values("count", ascending=False)
    if categories.empty:
        categories = pd.DataFrame({"skill_category": ["Unknown"], "count": [0]})

    chart_a, chart_b = st.columns(2)
    with chart_a:
        st.markdown('<div class="section-title">Top Skills</div>', unsafe_allow_html=True)
        st.plotly_chart(make_bar_chart(skills.head(12), x="count", y="skill", title="Top Skills", orientation="h", color="count"), use_container_width=True)
    with chart_b:
        st.markdown('<div class="section-title">Top Skill Categories</div>', unsafe_allow_html=True)
        st.plotly_chart(make_pie_chart(categories, names="skill_category", values="count", title="Skill Categories"), use_container_width=True)

    chart_c, chart_d = st.columns(2)
    with chart_c:
        st.markdown('<div class="section-title">Most Demanded Skills</div>', unsafe_allow_html=True)
        if not skills.empty:
            st.plotly_chart(make_treemap(skills.head(12).rename(columns={"skill": "Skill", "count": "Count"}), path=[px.Constant("Skills"), "Skill"], values="Count", title="Skill Treemap"), use_container_width=True)
    with chart_d:
        st.markdown('<div class="section-title">Skill Distribution</div>', unsafe_allow_html=True)
        skill_dist = filtered[filtered["skill_primary"] != "Unknown"]
        if skill_dist.empty:
            st.info("No skill distribution data available.")
        else:
            st.plotly_chart(make_histogram(skill_dist, x="skill_primary", color=None, title="Skill Distribution", height=360), use_container_width=True)

    role_skill = _role_skill_matrix(filtered)
    location_skill = _location_skill_matrix(filtered)
    extra_a, extra_b = st.columns(2)
    with extra_a:
        st.markdown('<div class="section-title">Skill vs Role Heatmap</div>', unsafe_allow_html=True)
        if role_skill.empty:
            st.info("No role-skill intersections were found.")
        else:
            st.plotly_chart(make_heatmap(role_skill, x="skill", y="role", z="count", title="Skill vs Role"), use_container_width=True)
    with extra_b:
        st.markdown('<div class="section-title">Skill vs Location Heatmap</div>', unsafe_allow_html=True)
        if location_skill.empty:
            st.info("No location-skill intersections were found.")
        else:
            st.plotly_chart(make_heatmap(location_skill, x="skill", y="location", z="count", title="Skill vs Location"), use_container_width=True)

    chart_e, chart_f = st.columns(2)
    with chart_e:
        st.markdown('<div class="section-title">Skill Sunburst</div>', unsafe_allow_html=True)
        if not skills.empty:
            sunburst_data = filtered.copy()
            sunburst_data["skill_primary"] = sunburst_data["skill_primary"].replace("Unknown", "Other")
            sunburst_data["role_primary"] = sunburst_data["role_primary"].replace("Unknown", "Other")
            sunburst_group = sunburst_data.groupby(["skill_category", "role_primary"]).size().reset_index(name="count")
            st.plotly_chart(make_sunburst(sunburst_group, path=["skill_category", "role_primary"], values="count", title="Skill Sunburst"), use_container_width=True)
    with chart_f:
        st.markdown('<div class="section-title">Top Skills by Company</div>', unsafe_allow_html=True)
        company_skill = filtered[filtered["company_primary"] != "Unknown"]
        if company_skill.empty:
            st.info("No company mentions were found in the filtered data.")
        else:
            exploded_skill = company_skill[["company_primary", "skill"]].copy()
            exploded_skill["skill"] = exploded_skill["skill"].apply(_split_multi_value)
            exploded_skill = exploded_skill.explode("skill")
            exploded_skill["skill"] = exploded_skill["skill"].apply(_strip_unknown)
            top_company_skill = exploded_skill.groupby(["company_primary", "skill"]).size().reset_index(name="count").sort_values("count", ascending=False).head(20)
            st.plotly_chart(make_treemap(top_company_skill.rename(columns={"company_primary": "Company", "skill": "Skill", "count": "Count"}), path=["Company", "Skill"], values="Count", title="Company vs Skill"), use_container_width=True)

    chart_g, chart_h = st.columns(2)
    with chart_g:
        st.markdown('<div class="section-title">Top Skills by Sentiment</div>', unsafe_allow_html=True)
        skill_sentiment = filtered[filtered["skill_primary"] != "Unknown"]
        if skill_sentiment.empty:
            st.info("No skill sentiment data available.")
        else:
            skill_sentiment = skill_sentiment.groupby(["skill_primary", "sentiment"]).size().reset_index(name="count")
            st.plotly_chart(make_bar_chart(skill_sentiment, x="count", y="skill_primary", color="sentiment", title="Skill by Sentiment", orientation="h"), use_container_width=True)
    with chart_h:
        st.markdown('<div class="section-title">Skill Search</div>', unsafe_allow_html=True)
        skill_query = st.text_input("Search skill", key="skills_page_search")
        search_df = filtered.copy()
        if skill_query:
            search_df = search_df[search_df["search_blob"].str.contains(re.escape(skill_query), case=False, na=False, regex=True)]
        st.dataframe(search_df[["timestamp", "title", "role", "skill", "location", "company", "sentiment", "subreddit"]].head(25), use_container_width=True, hide_index=True)

    render_paginated_table(skills.rename(columns={"skill": "Skill", "count": "Count"}), table_key="skills_frequency_table", columns=["Skill", "Count"], title="Skill Frequency Table", export_name="skill_frequency_table.csv", search_hint="Search skills")


def render_locations_page(df: pd.DataFrame, filtered_df: pd.DataFrame | None = None) -> None:
    inject_dashboard_styles()
    page_header("Locations and Market Coverage", "Geographic demand signals based on city-level mentions, normalized states, and relationships between locations, skills, and roles.")
    filtered = filtered_df if filtered_df is not None else apply_sidebar_filters(df)
    render_filter_summary(filtered, df)

    top_cities = count_multi_value(filtered, "location", top_n=15)
    top_states = filtered.groupby("location_state").size().reset_index(name="count").query("location_state != 'Unknown'").sort_values("count", ascending=False)
    chart_a, chart_b = st.columns(2)
    with chart_a:
        st.markdown('<div class="section-title">Top Hiring Cities</div>', unsafe_allow_html=True)
        st.plotly_chart(make_bar_chart(top_cities.head(12), x="count", y="location", title="Top Hiring Cities", orientation="h", color="count"), use_container_width=True)
    with chart_b:
        st.markdown('<div class="section-title">Top Hiring States</div>', unsafe_allow_html=True)
        if top_states.empty:
            st.info("No state-level data available.")
        else:
            st.plotly_chart(make_bar_chart(top_states.head(12), x="count", y="location_state", title="Top Hiring States", orientation="h", color="count"), use_container_width=True)

    chart_c, chart_d = st.columns(2)
    with chart_c:
        st.markdown('<div class="section-title">Location Distribution</div>', unsafe_allow_html=True)
        st.plotly_chart(make_pie_chart(top_cities.head(8), names="location", values="count", title="Location Distribution"), use_container_width=True)
    with chart_d:
        st.markdown('<div class="section-title">Location Treemap</div>', unsafe_allow_html=True)
        if top_cities.empty:
            st.info("No location data available.")
        else:
            st.plotly_chart(make_treemap(top_cities.head(12).rename(columns={"location": "Location", "count": "Count"}), path=[px.Constant("Locations"), "Location"], values="Count", title="Location Treemap"), use_container_width=True)

    location_role = _role_location_matrix(filtered)
    location_skill = _location_skill_matrix(filtered)
    chart_e, chart_f = st.columns(2)
    with chart_e:
        st.markdown('<div class="section-title">Location Heatmap</div>', unsafe_allow_html=True)
        if location_role.empty:
            st.info("No location-role intersections were found.")
        else:
            st.plotly_chart(make_heatmap(location_role, x="location", y="role", z="count", title="Location vs Role"), use_container_width=True)
    with chart_f:
        st.markdown('<div class="section-title">Location vs Skills</div>', unsafe_allow_html=True)
        if location_skill.empty:
            st.info("No location-skill intersections were found.")
        else:
            st.plotly_chart(make_heatmap(location_skill, x="skill", y="location", z="count", title="Location vs Skills"), use_container_width=True)

    chart_g, chart_h = st.columns(2)
    with chart_g:
        st.markdown('<div class="section-title">Location Search</div>', unsafe_allow_html=True)
        location_query = st.text_input("Search location", key="location_page_search")
        search_df = filtered.copy()
        if location_query:
            search_df = search_df[search_df["search_blob"].str.contains(re.escape(location_query), case=False, na=False, regex=True)]
        st.dataframe(search_df[["timestamp", "title", "role", "skill", "location", "company", "subreddit"]].head(25), use_container_width=True, hide_index=True)
    with chart_h:
        st.markdown('<div class="section-title">Top Companies by Location</div>', unsafe_allow_html=True)
        company_location = filtered[filtered["company_primary"] != "Unknown"]
        if company_location.empty:
            st.info("No company mentions were found in the filtered data.")
        else:
            exploded = company_location[["company_primary", "location"]].copy()
            exploded["location"] = exploded["location"].apply(_split_multi_value)
            exploded = exploded.explode("location")
            exploded["location"] = exploded["location"].apply(_strip_unknown)
            exploded = exploded[exploded["location"] != "Unknown"]
            top_company_location = exploded.groupby(["company_primary", "location"]).size().reset_index(name="count").sort_values("count", ascending=False).head(20)
            st.plotly_chart(make_treemap(top_company_location.rename(columns={"company_primary": "Company", "location": "Location", "count": "Count"}), path=["Company", "Location"], values="Count", title="Company by Location"), use_container_width=True)

    render_paginated_table(top_cities.rename(columns={"location": "Location", "count": "Count"}), table_key="location_table", columns=["Location", "Count"], title="Location Frequency Table", export_name="location_frequency_table.csv", search_hint="Search locations")


def render_roles_page(df: pd.DataFrame, filtered_df: pd.DataFrame | None = None) -> None:
    inject_dashboard_styles()
    page_header("Roles", "Role discovery, role mix, and role-driven relationships across skills, locations, and posting timelines.")
    filtered = filtered_df if filtered_df is not None else apply_sidebar_filters(df)
    render_filter_summary(filtered, df)

    roles = top_counts(filtered, "role", top_n=15)
    chart_a, chart_b = st.columns(2)
    with chart_a:
        st.markdown('<div class="section-title">Top Roles</div>', unsafe_allow_html=True)
        st.plotly_chart(make_bar_chart(roles.head(12), x="count", y="role", title="Top Roles", orientation="h", color="count"), use_container_width=True)
    with chart_b:
        st.markdown('<div class="section-title">Role Distribution</div>', unsafe_allow_html=True)
        st.plotly_chart(make_pie_chart(roles.head(8), names="role", values="count", title="Role Distribution"), use_container_width=True)

    role_skill = _role_skill_matrix(filtered)
    role_location = _role_location_matrix(filtered)
    chart_c, chart_d = st.columns(2)
    with chart_c:
        st.markdown('<div class="section-title">Role vs Skills</div>', unsafe_allow_html=True)
        if role_skill.empty:
            st.info("No role-skill intersections were found.")
        else:
            st.plotly_chart(make_heatmap(role_skill, x="skill", y="role", z="count", title="Role vs Skills"), use_container_width=True)
    with chart_d:
        st.markdown('<div class="section-title">Role vs Location</div>', unsafe_allow_html=True)
        if role_location.empty:
            st.info("No role-location intersections were found.")
        else:
            st.plotly_chart(make_heatmap(role_location, x="location", y="role", z="count", title="Role vs Location"), use_container_width=True)

    chart_e, chart_f = st.columns(2)
    with chart_e:
        st.markdown('<div class="section-title">Role Timeline</div>', unsafe_allow_html=True)
        timeline = make_time_series(filtered, period="M")
        if timeline.empty:
            st.info("No timeline data available.")
        else:
            st.plotly_chart(make_line_chart(timeline, x="date", y="count", title="Role Timeline"), use_container_width=True)
    with chart_f:
        st.markdown('<div class="section-title">Role Pie Chart</div>', unsafe_allow_html=True)
        if roles.empty:
            st.info("No role data available.")
        else:
            st.plotly_chart(make_pie_chart(roles.head(8), names="role", values="count", title="Role Mix"), use_container_width=True)

    chart_g, chart_h = st.columns(2)
    with chart_g:
        st.markdown('<div class="section-title">Role Heatmap</div>', unsafe_allow_html=True)
        if role_skill.empty:
            st.info("No role heatmap data available.")
        else:
            st.plotly_chart(make_heatmap(role_skill, x="skill", y="role", z="count", title="Role Heatmap"), use_container_width=True)
    with chart_h:
        st.markdown('<div class="section-title">Role Search</div>', unsafe_allow_html=True)
        role_query = st.text_input("Search role", key="role_page_search")
        search_df = filtered.copy()
        if role_query:
            search_df = search_df[search_df["search_blob"].str.contains(re.escape(role_query), case=False, na=False, regex=True)]
        st.dataframe(search_df[["timestamp", "title", "role", "skill", "location", "company", "sentiment", "subreddit"]].head(25), use_container_width=True, hide_index=True)

    render_paginated_table(roles.rename(columns={"role": "Role", "count": "Count"}), table_key="role_table", columns=["Role", "Count"], title="Role Frequency Table", export_name="role_table.csv", search_hint="Search roles")


def render_companies_page(df: pd.DataFrame, filtered_df: pd.DataFrame | None = None) -> None:
    inject_dashboard_styles()
    page_header("Companies", "Company mentions inferred from post titles and keywords, with role and skill relationships for employer-focused analysis.")
    filtered = filtered_df if filtered_df is not None else apply_sidebar_filters(df)
    render_filter_summary(filtered, df)

    company_df = filtered[filtered["company_primary"] != "Unknown"].copy()
    top_companies = top_counts(company_df, "company_primary", top_n=20)
    chart_a, chart_b = st.columns(2)
    with chart_a:
        st.markdown('<div class="section-title">Top Companies</div>', unsafe_allow_html=True)
        if top_companies.empty:
            st.info("No company mentions were found in the filtered data.")
        else:
            st.plotly_chart(make_bar_chart(top_companies.head(12), x="count", y="company_primary", title="Top Companies", orientation="h", color="count"), use_container_width=True)
    with chart_b:
        st.markdown('<div class="section-title">Company Mentions</div>', unsafe_allow_html=True)
        if top_companies.empty:
            st.info("No company mentions were found in the filtered data.")
        else:
            st.plotly_chart(make_pie_chart(top_companies.head(8), names="company_primary", values="count", title="Company Mentions"), use_container_width=True)

    chart_c, chart_d = st.columns(2)
    with chart_c:
        st.markdown('<div class="section-title">Company Timeline</div>', unsafe_allow_html=True)
        if company_df.empty:
            st.info("No timeline data available.")
        else:
            timeline = company_df.copy()
            timeline["date"] = timeline["timestamp"].dt.to_period("M").dt.to_timestamp()
            timeline = timeline.groupby(["date", "company_primary"]).size().reset_index(name="count")
            st.plotly_chart(make_line_chart(timeline, x="date", y="count", color="company_primary", title="Company Timeline"), use_container_width=True)
    with chart_d:
        st.markdown('<div class="section-title">Company vs Roles</div>', unsafe_allow_html=True)
        if company_df.empty:
            st.info("No company-role intersections were found.")
        else:
            company_role = company_df.groupby(["company_primary", "role_primary"]).size().reset_index(name="count").sort_values("count", ascending=False).head(25)
            st.plotly_chart(make_treemap(company_role.rename(columns={"company_primary": "Company", "role_primary": "Role", "count": "Count"}), path=["Company", "Role"], values="Count", title="Company vs Role"), use_container_width=True)

    chart_e, chart_f = st.columns(2)
    with chart_e:
        st.markdown('<div class="section-title">Company vs Skills</div>', unsafe_allow_html=True)
        if company_df.empty:
            st.info("No company-skill intersections were found.")
        else:
            exploded = company_df[["company_primary", "skill"]].copy()
            exploded["skill"] = exploded["skill"].apply(_split_multi_value)
            exploded = exploded.explode("skill")
            exploded["skill"] = exploded["skill"].apply(_strip_unknown)
            exploded = exploded[exploded["skill"] != "Unknown"]
            company_skill = exploded.groupby(["company_primary", "skill"]).size().reset_index(name="count").sort_values("count", ascending=False).head(25)
            st.plotly_chart(make_treemap(company_skill.rename(columns={"company_primary": "Company", "skill": "Skill", "count": "Count"}), path=["Company", "Skill"], values="Count", title="Company vs Skill"), use_container_width=True)
    with chart_f:
        st.markdown('<div class="section-title">Search Company</div>', unsafe_allow_html=True)
        company_query = st.text_input("Search company", key="company_page_search")
        search_df = company_df.copy()
        if company_query:
            search_df = search_df[search_df["search_blob"].str.contains(re.escape(company_query), case=False, na=False, regex=True)]
        st.dataframe(search_df[["timestamp", "title", "company", "role", "skill", "location", "sentiment", "subreddit"]].head(25), use_container_width=True, hide_index=True)

    render_paginated_table(top_companies.rename(columns={"company_primary": "Company", "count": "Count"}), table_key="company_table", columns=["Company", "Count"], title="Company Frequency Table", export_name="company_table.csv", search_hint="Search companies")


def render_sentiment_page(df: pd.DataFrame, filtered_df: pd.DataFrame | None = None) -> None:
    inject_dashboard_styles()
    page_header("Sentiment", "Sentiment distribution and sentiment relationships across roles, skills, companies, and time.")
    filtered = filtered_df if filtered_df is not None else apply_sidebar_filters(df)
    render_filter_summary(filtered, df)

    sentiment_counts = top_counts(filtered, "sentiment", top_n=10)
    chart_a, chart_b = st.columns(2)
    with chart_a:
        st.markdown('<div class="section-title">Sentiment Breakdown</div>', unsafe_allow_html=True)
        st.plotly_chart(make_bar_chart(sentiment_counts, x="count", y="sentiment", title="Sentiment Bar", orientation="h", color="count"), use_container_width=True)
    with chart_b:
        st.markdown('<div class="section-title">Pie Chart</div>', unsafe_allow_html=True)
        st.plotly_chart(make_pie_chart(sentiment_counts, names="sentiment", values="count", title="Sentiment Pie"), use_container_width=True)

    chart_c, chart_d = st.columns(2)
    with chart_c:
        st.markdown('<div class="section-title">Timeline</div>', unsafe_allow_html=True)
        sentiment_timeline = filtered.dropna(subset=["timestamp"]).copy()
        if sentiment_timeline.empty:
            st.info("No timeline data available.")
        else:
            sentiment_timeline["date"] = sentiment_timeline["timestamp"].dt.to_period("M").dt.to_timestamp()
            sentiment_timeline = sentiment_timeline.groupby(["date", "sentiment"]).size().reset_index(name="count")
            st.plotly_chart(make_line_chart(sentiment_timeline, x="date", y="count", color="sentiment", title="Sentiment Timeline"), use_container_width=True)
    with chart_d:
        st.markdown('<div class="section-title">Sentiment by Role</div>', unsafe_allow_html=True)
        if filtered.empty:
            st.info("No sentiment-role intersections were found.")
        else:
            sentiment_role = filtered.groupby(["role_primary", "sentiment"]).size().reset_index(name="count")
            st.plotly_chart(make_bar_chart(sentiment_role, x="count", y="role_primary", color="sentiment", title="Sentiment by Role", orientation="h"), use_container_width=True)

    chart_e, chart_f = st.columns(2)
    with chart_e:
        st.markdown('<div class="section-title">Sentiment by Skill</div>', unsafe_allow_html=True)
        skill_rows = filtered[filtered["skill_primary"] != "Unknown"]
        if skill_rows.empty:
            st.info("No sentiment-skill intersections were found.")
        else:
            sentiment_skill = skill_rows.groupby(["skill_primary", "sentiment"]).size().reset_index(name="count")
            st.plotly_chart(make_bar_chart(sentiment_skill, x="count", y="skill_primary", color="sentiment", title="Sentiment by Skill", orientation="h"), use_container_width=True)
    with chart_f:
        st.markdown('<div class="section-title">Sentiment by Company</div>', unsafe_allow_html=True)
        company_rows = filtered[filtered["company_primary"] != "Unknown"]
        if company_rows.empty:
            st.info("No company mentions were found in the filtered data.")
        else:
            sentiment_company = company_rows.groupby(["company_primary", "sentiment"]).size().reset_index(name="count")
            st.plotly_chart(make_bar_chart(sentiment_company, x="count", y="company_primary", color="sentiment", title="Sentiment by Company", orientation="h"), use_container_width=True)

    render_paginated_table(sentiment_counts.rename(columns={"sentiment": "Sentiment", "count": "Count"}), table_key="sentiment_table", columns=["Sentiment", "Count"], title="Sentiment Frequency Table", export_name="sentiment_table.csv", search_hint="Search sentiment")


def render_topics_page(df: pd.DataFrame, filtered_df: pd.DataFrame | None = None) -> None:
    inject_dashboard_styles()
    page_header("Topic Modeling", "Heuristic topic clusters built from post text, roles, skills, and locations to surface dominant discussion themes.")
    filtered = filtered_df if filtered_df is not None else apply_sidebar_filters(df)
    render_filter_summary(filtered, df)

    topics = filtered.groupby("topic_display").size().reset_index(name="count").sort_values("count", ascending=False)
    topic_keywords = _topic_keyword_frame(filtered)

    chart_a, chart_b = st.columns(2)
    with chart_a:
        st.markdown('<div class="section-title">Top Topics</div>', unsafe_allow_html=True)
        st.plotly_chart(make_bar_chart(topics.head(12), x="count", y="topic_display", title="Top Topics", orientation="h", color="count"), use_container_width=True)
    with chart_b:
        st.markdown('<div class="section-title">Topic Distribution</div>', unsafe_allow_html=True)
        st.plotly_chart(make_pie_chart(topics.head(8), names="topic_display", values="count", title="Topic Distribution"), use_container_width=True)

    chart_c, chart_d = st.columns(2)
    with chart_c:
        st.markdown('<div class="section-title">Topic Keywords</div>', unsafe_allow_html=True)
        if topic_keywords.empty:
            st.info("No topic keyword data available.")
        else:
            st.dataframe(topic_keywords.rename(columns={"topic_display": "Topic", "count": "Count", "keywords": "Keywords"}), use_container_width=True, hide_index=True)
    with chart_d:
        st.markdown('<div class="section-title">Topic vs Sentiment</div>', unsafe_allow_html=True)
        if filtered.empty:
            st.info("No topic-sentiment intersections were found.")
        else:
            topic_sentiment = filtered.groupby(["topic_display", "sentiment"]).size().reset_index(name="count")
            st.plotly_chart(make_bar_chart(topic_sentiment, x="count", y="topic_display", color="sentiment", title="Topic vs Sentiment", orientation="h"), use_container_width=True)

    chart_e, chart_f = st.columns(2)
    with chart_e:
        st.markdown('<div class="section-title">Topic vs Skills</div>', unsafe_allow_html=True)
        topic_skill_df = filtered[filtered["skill_primary"] != "Unknown"]
        if topic_skill_df.empty:
            st.info("No topic-skill intersections were found.")
        else:
            topic_skill = topic_skill_df.groupby(["topic_display", "skill_primary"]).size().reset_index(name="count").sort_values("count", ascending=False).head(30)
            st.plotly_chart(make_treemap(topic_skill.rename(columns={"topic_display": "Topic", "skill_primary": "Skill", "count": "Count"}), path=["Topic", "Skill"], values="Count", title="Topic vs Skills"), use_container_width=True)
    with chart_f:
        st.markdown('<div class="section-title">Topic Table</div>', unsafe_allow_html=True)
        st.dataframe(topics.rename(columns={"topic_display": "Topic", "count": "Count"}), use_container_width=True, hide_index=True)

    render_paginated_table(topics.rename(columns={"topic_display": "Topic", "count": "Count"}), table_key="topic_table", columns=["Topic", "Count"], title="Topic Frequency Table", export_name="topic_table.csv", search_hint="Search topics")


def render_trends_page(df: pd.DataFrame, filtered_df: pd.DataFrame | None = None) -> None:
    inject_dashboard_styles()
    page_header("Trends", "Time-series views for volume, roles, skills, companies, locations, and sentiment changes across the dataset lifecycle.")
    filtered = filtered_df if filtered_df is not None else apply_sidebar_filters(df)
    render_filter_summary(filtered, df)

    monthly = make_time_series(filtered, period="M")
    weekly = make_time_series(filtered, period="W")
    chart_a, chart_b = st.columns(2)
    with chart_a:
        st.markdown('<div class="section-title">Posts per Month</div>', unsafe_allow_html=True)
        if monthly.empty:
            st.info("No monthly data available.")
        else:
            st.plotly_chart(make_line_chart(monthly, x="date", y="count", title="Posts per Month"), use_container_width=True)
    with chart_b:
        st.markdown('<div class="section-title">Posts per Week</div>', unsafe_allow_html=True)
        if weekly.empty:
            st.info("No weekly data available.")
        else:
            st.plotly_chart(make_line_chart(weekly, x="date", y="count", title="Posts per Week"), use_container_width=True)

    chart_c, chart_d = st.columns(2)
    with chart_c:
        st.markdown('<div class="section-title">Hiring Trend</div>', unsafe_allow_html=True)
        hiring_trend = filtered.groupby("month").size().reset_index(name="count").rename(columns={"month": "date"})
        if hiring_trend.empty:
            st.info("No hiring trend data available.")
        else:
            st.plotly_chart(make_line_chart(hiring_trend, x="date", y="count", title="Hiring Trend"), use_container_width=True)
    with chart_d:
        st.markdown('<div class="section-title">Skill Trend</div>', unsafe_allow_html=True)
        skill_trend = filtered.groupby(["month", "skill_primary"]).size().reset_index(name="count").rename(columns={"month": "date"})
        if skill_trend.empty:
            st.info("No skill trend data available.")
        else:
            st.plotly_chart(make_line_chart(skill_trend, x="date", y="count", color="skill_primary", title="Skill Trend"), use_container_width=True)

    chart_e, chart_f = st.columns(2)
    with chart_e:
        st.markdown('<div class="section-title">Role Trend</div>', unsafe_allow_html=True)
        role_trend = filtered.groupby(["month", "role_primary"]).size().reset_index(name="count").rename(columns={"month": "date"})
        if role_trend.empty:
            st.info("No role trend data available.")
        else:
            st.plotly_chart(make_line_chart(role_trend, x="date", y="count", color="role_primary", title="Role Trend"), use_container_width=True)
    with chart_f:
        st.markdown('<div class="section-title">Company Trend</div>', unsafe_allow_html=True)
        company_trend = filtered[filtered["company_primary"] != "Unknown"].groupby(["month", "company_primary"]).size().reset_index(name="count").rename(columns={"month": "date"})
        if company_trend.empty:
            st.info("No company trend data available.")
        else:
            st.plotly_chart(make_line_chart(company_trend, x="date", y="count", color="company_primary", title="Company Trend"), use_container_width=True)

    chart_g, chart_h = st.columns(2)
    with chart_g:
        st.markdown('<div class="section-title">Location Trend</div>', unsafe_allow_html=True)
        location_trend = filtered.groupby(["month", "location_primary"]).size().reset_index(name="count").rename(columns={"month": "date"})
        if location_trend.empty:
            st.info("No location trend data available.")
        else:
            st.plotly_chart(make_line_chart(location_trend, x="date", y="count", color="location_primary", title="Location Trend"), use_container_width=True)
    with chart_h:
        st.markdown('<div class="section-title">Sentiment Trend</div>', unsafe_allow_html=True)
        sentiment_trend = filtered.groupby(["month", "sentiment"]).size().reset_index(name="count").rename(columns={"month": "date"})
        if sentiment_trend.empty:
            st.info("No sentiment trend data available.")
        else:
            st.plotly_chart(make_line_chart(sentiment_trend, x="date", y="count", color="sentiment", title="Sentiment Trend"), use_container_width=True)


def render_search_page(df: pd.DataFrame, filtered_df: pd.DataFrame | None = None) -> None:
    inject_dashboard_styles()
    page_header("Search Posts", "Global search across the filtered dataset with role, skill, location, company, subreddit, and keyword matching.")
    filtered = filtered_df if filtered_df is not None else apply_sidebar_filters(df)
    render_filter_summary(filtered, df)

    st.markdown('<div class="section-title">Global Search</div>', unsafe_allow_html=True)
    global_query = st.text_input("Search across title, role, skill, location, company, subreddit, sentiment, topic, and keyword", key="global_search_query")
    search_df = search_dataframe(filtered, global_query)

    filters_col_1, filters_col_2, filters_col_3 = st.columns(3)
    with filters_col_1:
        role_pick = st.multiselect("Role", _sorted_options(search_df["role"]), default=[], key="search_role_pick")
        skill_pick = st.multiselect("Skill", _sorted_options(pd.Series([item for row in search_df["skill"].apply(_split_multi_value) for item in row])), default=[], key="search_skill_pick")
    with filters_col_2:
        location_pick = st.multiselect("Location", _sorted_options(pd.Series([item for row in search_df["location"].apply(_split_multi_value) for item in row])), default=[], key="search_location_pick")
        company_pick = st.multiselect("Company", _sorted_options(pd.Series([item for row in search_df["company_list"].apply(lambda items: items if isinstance(items, list) else []) for item in row])), default=[], key="search_company_pick")
    with filters_col_3:
        subreddit_pick = st.multiselect("Subreddit", _sorted_options(search_df["subreddit"]), default=[], key="search_subreddit_pick")
        keyword_pick = st.text_input("Keyword contains", key="search_keyword_pick")

    if role_pick:
        search_df = search_df[search_df["role"].isin(role_pick)]
    if skill_pick:
        search_df = _filter_multi_value(search_df, "skill", skill_pick)
    if location_pick:
        search_df = _filter_multi_value(search_df, "location", location_pick)
    if company_pick:
        search_df = _filter_multi_value(search_df, "company_list", company_pick)
    if subreddit_pick:
        search_df = search_df[search_df["subreddit"].isin(subreddit_pick)]
    if keyword_pick:
        search_df = search_df[search_df["keyword"].str.contains(re.escape(keyword_pick), case=False, na=False, regex=True)]

    date_col_1, date_col_2 = st.columns(2)
    with date_col_1:
        start_date = st.date_input("Start date", value=search_df["timestamp"].min().date() if search_df["timestamp"].notna().any() else pd.Timestamp.today().date(), key="search_start_date")
    with date_col_2:
        end_date = st.date_input("End date", value=search_df["timestamp"].max().date() if search_df["timestamp"].notna().any() else pd.Timestamp.today().date(), key="search_end_date")
    search_df = search_df[(search_df["timestamp"].dt.date >= start_date) & (search_df["timestamp"].dt.date <= end_date)]

    st.markdown('<div class="section-title">Filtered Results</div>', unsafe_allow_html=True)
    columns = ["timestamp", "title", "role", "skill", "location", "company", "sentiment", "topic_display", "subreddit", "keyword", "post_url"]
    render_paginated_table(search_df[columns], table_key="search_table", columns=columns, title="Search Results", export_name="search_results.csv", search_hint="Search within results")