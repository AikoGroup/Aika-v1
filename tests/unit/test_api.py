"""
Unit tests for the API endpoints.
"""

import pytest
from fastapi.testclient import TestClient


@pytest.mark.api
def test_root_endpoint(test_client: TestClient):
    """Test the root endpoint."""
    response = test_client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Aika AI System"
    assert data["version"] == "0.1.0"
    assert data["status"] == "operational"


@pytest.mark.api
def test_health_check(test_client: TestClient):
    """Test the health check endpoint."""
    response = test_client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
