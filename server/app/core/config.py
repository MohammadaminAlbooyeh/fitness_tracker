"""Application configuration settings"""

from pydantic import BaseModel

class Settings(BaseModel):
    # Database
    database_url: str = "sqlite:///./test.db"

    # Security
    secret_key: str = "test-secret-key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Health API keys (mock for testing)
    fitbit_client_id: str = "mock"
    fitbit_client_secret: str = "mock"
    apple_health_client_id: str = "mock"
    apple_health_client_secret: str = "mock"

settings = Settings()