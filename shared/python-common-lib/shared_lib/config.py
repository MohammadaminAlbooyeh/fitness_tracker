"""Configuration settings."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://user:password@localhost/ecommerce"
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    redis_url: str = "redis://localhost:6379/0"
    service_name: str = "service"
    # Kafka (MSK) configuration. bootstrap servers can be overridden via the
    # KAFKA_BROKERS env var (also referenced in k8s configmap & docker-compose).
    kafka_bootstrap_servers: str = "localhost:9092"
    # Gate the in-process Kafka consumer so unit tests and local runs without a
    # broker stay unaffected. Enable in production via KAFKA_CONSUMER_ENABLED=true.
    kafka_consumer_enabled: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
