from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    google_api_key: str
    upload_dir: str = "uploads"
    gmail_address: str = ""
    gmail_app_password: str = ""

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
