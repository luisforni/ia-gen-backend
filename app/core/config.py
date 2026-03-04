from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = Field(default="IA Gen Backend")
    OLLAMA_HOST: str = Field(default="http://localhost:11434")
    MODEL_NAME: str = Field(default="llama2")
    PORT: int = Field(default=8000)
    ENVIRONMENT: str = Field(default="development")
    DEBUG: bool = Field(default=False)
    LOG_LEVEL: str = Field(default="INFO")
    ALLOWED_ORIGINS: str = Field(default="http://localhost:3000,http://localhost:8000")
    REDIS_URL: str = Field(default="redis://localhost:6379/0")
    RATE_LIMIT_ENABLED: bool = Field(default=True)
    RATE_LIMIT_REQUESTS: int = Field(default=10)
    RATE_LIMIT_PERIOD: int = Field(default=3600)
    
    def get_allowed_origins(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()