"""
Pytest configuration for the Aika AI System tests.
"""

import os
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from src.api.main import app


@pytest.fixture
def test_client():
    """
    Create a FastAPI test client.
    
    Returns:
        TestClient: FastAPI test client
    """
    return TestClient(app)


@pytest.fixture
def mock_env_vars():
    """
    Mock environment variables for testing.
    
    Yields:
        None
    """
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


@pytest.fixture
def mock_supabase_client():
    """
    Mock Supabase client for testing.
    
    Yields:
        MagicMock: Mocked Supabase client
    """
    with patch("src.database.connection.create_client") as mock_create_client:
        mock_client = mock_create_client.return_value
        mock_table = mock_client.table.return_value
        mock_select = mock_table.select.return_value
        mock_execute = mock_select.execute.return_value
        
        # Configure the mock to return a test result
        mock_execute.data = [{"id": "test_id", "name": "test_name"}]
        
        yield mock_client
