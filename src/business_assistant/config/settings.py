"""Application settings module."""
import os
from dataclasses import dataclass


@dataclass
class ServerSettings:
    """Server configuration settings."""
    host: str = os.getenv("SERVER_HOST", "0.0.0.0")
    port: int = int(os.getenv("SERVER_PORT", "8000"))
    reload: bool = bool(os.getenv("SERVER_RELOAD", "True"))
