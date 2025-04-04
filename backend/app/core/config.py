from pydantic_settings import BaseSettings
from typing import List, Optional
from pydantic import AnyHttpUrl, validator

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/bilancismart"
    
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "BilanciSmart"
    VERSION: str = "1.0.0"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"  # Cambiare in produzione!
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 giorni
    
    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",  # Frontend React
        "http://localhost:8501",  # Streamlit
    ]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 