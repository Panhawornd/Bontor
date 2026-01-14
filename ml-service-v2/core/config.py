"""Configuration settings for ML Service"""
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DB_HOST: str = "localhost"
    DB_PORT: str = "5433"
    DB_NAME: str = "grade_analyzer"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "baboo123"
    
    # Models
    MODEL_DIR: str = "models"
    SENTENCE_MODEL: str = "all-MiniLM-L6-v2"
    ZEROSHOT_MODEL: str = "facebook/bart-large-mnli"
    
    class Config:
        env_file = ".env"

settings = Settings()
