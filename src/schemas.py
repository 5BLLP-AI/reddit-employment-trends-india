from pydantic import BaseModel
from typing import Optional


class Submission(BaseModel):
    id: str
    title: str
    selftext: Optional[str]
    created_utc: float
