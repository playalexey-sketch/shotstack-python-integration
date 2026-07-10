"""Configuration management for Shotstack API client."""

import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv()

ENVIRONMENTS = {
    "stage": "https://api.shotstack.io/stage",
    "production": "https://api.shotstack.io/v1",
}


@dataclass
class ShotstackConfig:
    """Configuration for Shotstack API client.

    Args:
        api_key: Shotstack API key. Falls back to SHOTSTACK_API_KEY env var.
        environment: API environment - 'stage' or 'production'.
        timeout: Request timeout in seconds.
    """

    api_key: str = field(default=None)
    environment: str = field(default="stage")
    timeout: int = field(default=30)

    def __post_init__(self):
        if not self.api_key:
            self.api_key = os.environ.get("SHOTSTACK_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key is required. Set SHOTSTACK_API_KEY environment variable "
                "or pass api_key parameter."
            )
        if self.environment not in ENVIRONMENTS:
            raise ValueError(
                f"Invalid environment '{self.environment}'. "
                f"Choose from: {', '.join(ENVIRONMENTS.keys())}"
            )

    @property
    def base_url(self) -> str:
        """Return base URL for the configured environment."""
        return ENVIRONMENTS[self.environment]
