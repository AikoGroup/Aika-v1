"""
Unit tests for configuration utilities.
"""

import os
from unittest.mock import patch

import pytest

from src.utils.config import Settings, get_settings


@pytest.fixture
def mock_env_vars():
    """Mock environment variables for testing."""
    with patch.dict(os.environ, {
        "DEBUG": "True",
        "LOG_LEVEL": "DEBUG",
        "SECRET_KEY": "test_secret_key",
        "ALLOWED_ORIGINS": "http://localhost:3000,http://localhost:8000",
        "SUPABASE_URL": "https://test.supabase.co",
        "SUPABASE_SERVICE_KEY": "test_service_key",
        "KAFKA_BOOTSTRAP_SERVERS": "localhost:9092",
        "ANTHROPIC_API_KEY": "test_anthropic_key",
        "PRIMARY_MODEL": "claude-3-opus-20240229",
        "REASONER_MODEL": "claude-3-sonnet-20240229",
        "SUMMARIZER_MODEL": "claude-3-haiku-20240307",
    }):
        yield


def test_settings_from_env(mock_env_vars):
    """Test that settings are loaded from environment variables."""
    settings = Settings()
    
    assert settings.DEBUG is True
    assert settings.LOG_LEVEL == "DEBUG"
    assert settings.SECRET_KEY == "test_secret_key"
    assert settings.ALLOWED_ORIGINS == ["http://localhost:3000", "http://localhost:8000"]
    assert settings.SUPABASE_URL == "https://test.supabase.co"
    assert settings.SUPABASE_SERVICE_KEY == "test_service_key"
    assert settings.KAFKA_BOOTSTRAP_SERVERS == "localhost:9092"
    assert settings.ANTHROPIC_API_KEY == "test_anthropic_key"
    assert settings.PRIMARY_MODEL == "claude-3-opus-20240229"
    assert settings.REASONER_MODEL == "claude-3-sonnet-20240229"
    assert settings.SUMMARIZER_MODEL == "claude-3-haiku-20240307"


def test_get_settings_caching(mock_env_vars):
    """Test that get_settings caches the settings instance."""
    settings1 = get_settings()
    settings2 = get_settings()
    
    assert settings1 is settings2  # Same instance


def test_allowed_origins_parsing():
    """Test that ALLOWED_ORIGINS is parsed correctly from string."""
    with patch.dict(os.environ, {
        "SECRET_KEY": "test_secret_key",
        "SUPABASE_URL": "https://test.supabase.co",
        "SUPABASE_SERVICE_KEY": "test_service_key",
        "ANTHROPIC_API_KEY": "test_anthropic_key",
        "ALLOWED_ORIGINS": "http://test1.com,http://test2.com",
    }):
        settings = Settings()
        assert settings.ALLOWED_ORIGINS == ["http://test1.com", "http://test2.com"]
