"""
Configuration settings for the application
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Canvas API Configuration
    CANVAS_API_BASE_URL: str = "https://queues.canvas.mgsops.net:8020"
    CANVAS_BEARER_TOKEN: str = ""
    
    # OpenAI API Configuration
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    
    # Azure OpenAI Configuration
    AZURE_OPENAI_API_KEY: str = ""
    AZURE_OPENAI_ENDPOINT: str = ""
    AZURE_OPENAI_DEPLOYMENT_NAME: str = "gpt-4o"
    AZURE_OPENAI_API_VERSION: str = "2024-05-01-preview"
    
    # Okta / Canvas auth (for getting Bearer tokens when CANVAS_BEARER_TOKEN is not set)
    OKTA_TOKEN_URL: str = ""
    OKTA_BASIC_AUTH: str = ""
    OKTA_USERNAME: str = ""
    OKTA_PASSWORD: str = ""
    OKTA_SCOPE: str = "openid roles"
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Create a global settings instance
settings = Settings()
