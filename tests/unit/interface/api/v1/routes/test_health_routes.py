"""Unit tests for health check endpoint."""
from datetime import datetime, timezone
from fastapi.testclient import TestClient
import pytest

from business_assistant.config.settings import settings
from business_assistant.infrastructure.web.app import create_app
from business_assistant.interface.api.v1.models.health_models import HealthResponse


@pytest.fixture
def client() -> TestClient:
    """Create a test client fixture."""
    app = create_app()
    return TestClient(app)


def test_health_check_endpoint(client: TestClient) -> None:
    """Test health check endpoint returns expected response."""
    # When
    response = client.get(f"{settings.api_prefix}/health")
    
    # Then
    assert response.status_code == 200
    health_data = response.json()
    
    # Validate response structure
    assert isinstance(health_data, dict)
    assert "status" in health_data
    assert "timestamp" in health_data
    assert "version" in health_data
    
    # Validate response values
    assert health_data["status"] == "ok"
    assert health_data["version"] == "1.0.0"
    
    # Validate timestamp is a valid datetime
    timestamp = datetime.fromisoformat(health_data["timestamp"].replace("Z", "+00:00"))
    assert isinstance(timestamp, datetime)
    assert timestamp.tzinfo is not None  # Ensure timezone-aware


def test_health_check_response_model() -> None:
    """Test health check response model validation."""
    # Given
    test_data = {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc),
        "version": "1.0.0"
    }
    
    # When
    health_response = HealthResponse(**test_data)
    
    # Then
    assert health_response.status == test_data["status"]
    assert health_response.timestamp == test_data["timestamp"]
    assert health_response.version == test_data["version"]
    assert health_response.timestamp.tzinfo is not None  # Ensure timezone-aware
