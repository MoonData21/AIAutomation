from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "AI Stock Analysis API"
    APP_ENV: str = "development"
    ANTHROPIC_API_KEY: str
    DATABASE_URL: str = "sqlite+aiosqlite:///./workflow.db"

    class Config:
        env_file = ".env"


settings = Settings()