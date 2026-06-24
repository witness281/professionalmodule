from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_TITLE: str = "BookStore API"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_NAME: str = "bookstore"
    
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    MAX_IMAGE_SIZE: int = 2_000_000  # 2 MB
    IMAGE_MAX_WIDTH: int = 400
    IMAGE_MAX_HEIGHT: int = 400
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()