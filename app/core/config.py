from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8001
    DEBUG: bool = True
    
    # Google Generative AI Configuration
    GOOGLE_API_KEY: Optional[str] = None
    
    # Model Configuration
    GEMINI_MODEL: str = "models/gemini-2.5-flash"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra environment variables

settings = Settings() 