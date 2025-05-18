from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    WAHA_URL: str = "http://localhost:3000"
    MODEL_NAME: str = "gpt-3.5-turbo"
    OPENAI_API_KEY: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings():
    return Settings() 