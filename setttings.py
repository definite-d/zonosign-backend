import datetime

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: bytes
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    @property
    def TZ(self):
        return datetime.UTC

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
