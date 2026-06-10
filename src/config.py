from pydantic import BaseSettings


class Settings(BaseSettings):
    reddit_client_id: str
    reddit_client_secret: str
    reddit_user_agent: str = "reddit-employment-trends/0.1"

    class Config:
        env_file = ".env"


settings = Settings()
