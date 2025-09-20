from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    app_name: str = "Automa"
    sqlite_url: str = Field(default="sqlite:///./automa.db")
    secret_key: str = Field(default="change-this-secret")
    jwt_algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=60)
    cors_origins: list[str] = Field(default_factory=lambda: ["*"])

    # bootstrap admin (for MVP)
    admin_email: str = Field(default="admin@example.com")
    admin_password: str = Field(default="admin")

    class Config:
        env_prefix = "AUTOMA_"


settings = Settings()

