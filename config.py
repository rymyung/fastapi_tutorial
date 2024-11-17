from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings): # 환경변수를 다루는 클래스
    model_config = SettingsConfigDict( # 환경변수를 .env로부터 읽어들임
        env_file=".env",
        env_file_encoding="utf-8"
    )

    database_username: str
    database_password: str
    jwt_secret: str

@lru_cache
def get_settings():
    return Settings()
