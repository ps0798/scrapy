from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    AUTH_TOKEN: str
    STATIC_DATA_PATH: str
    
    model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def get_settings():
    return Settings()