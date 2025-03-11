"""Health check domain model."""
from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class HealthStatus:
    """Health status domain model."""
    status: str
    timestamp: datetime
    version: str = "1.0.0"

    @classmethod
    def create_ok_status(cls) -> "HealthStatus":
        """Create a healthy status."""
        return cls(
            status="ok",
            timestamp=datetime.now(timezone.utc)
        )
