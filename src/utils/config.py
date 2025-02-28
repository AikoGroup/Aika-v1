"""
Configuration utilities for the Aika AI System.
"""

import os
from functools import lru_cache
from typing import List, Optional

from pydantic import AnyHttpUrl, BaseSettings, Field, validator


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # API Settings
    DEBUG: bool = Field(False, env="DEBUG")
    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALLOWED_ORIGINS: List[str] = Field(["http://localhost:3000", "http://localhost:8000"], env="ALLOWED_ORIGINS")
    
    # Database Settings
    SUPABASE_URL: str = Field(..., env="SUPABASE_URL")
    SUPABASE_SERVICE_KEY: str = Field(..., env="SUPABASE_SERVICE_KEY")
    
    # Kafka Settings
    KAFKA_BOOTSTRAP_SERVERS: str = Field("localhost:9092", env="KAFKA_BOOTSTRAP_SERVERS")
    
    # Anthropic API Settings
    ANTHROPIC_API_KEY: str = Field(..., env="ANTHROPIC_API_KEY")
    
    # Model Settings
    PRIMARY_MODEL: str = Field("claude-3-opus-20240229", env="PRIMARY_MODEL")
    REASONER_MODEL: str = Field("claude-3-sonnet-20240229", env="REASONER_MODEL")
    SUMMARIZER_MODEL: str = Field("claude-3-haiku-20240307", env="SUMMARIZER_MODEL")
    
    # LangSmith Settings (optional)
    LANGCHAIN_TRACING_V2: bool = Field(False, env="LANGCHAIN_TRACING_V2")
    LANGCHAIN_ENDPOINT: Optional[str] = Field(None, env="LANGCHAIN_ENDPOINT")
    LANGCHAIN_API_KEY: Optional[str] = Field(None, env="LANGCHAIN_API_KEY")
    LANGCHAIN_PROJECT: Optional[str] = Field(None, env="LANGCHAIN_PROJECT")
    
    @validator("ALLOWED_ORIGINS", pre=True)
    def parse_allowed_origins(cls, v):
        """Parse ALLOWED_ORIGINS from string to list if needed."""
        if isinstance(v, str):
            return v.split(",")
        return v
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Returns:
        Settings instance
    """
    return Settings()
