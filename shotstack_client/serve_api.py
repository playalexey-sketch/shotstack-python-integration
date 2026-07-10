"""Serve API for Shotstack asset management operations."""

from .config import ShotstackConfig


class ServeAPI:
    """API client for managing rendered assets."""

    def __init__(self, config: ShotstackConfig):
        self.config = config

    def _request(self, method: str, endpoint: str) -> dict:
        """Make an HTTP request to the Shotstack API."""
        import requests

        url = f"{self.config.base_url}/{endpoint}"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.config.api_key,
        }

        from .exceptions import (
            AuthenticationError,
            NotFoundError,
            RateLimitError,
            RenderError,
            ValidationError,
        )

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                timeout=self.config.timeout,
            )
        except requests.exceptions.RequestException as e:
            raise RenderError(f"Request failed: {e}")

        if response.status_code == 401:
            raise AuthenticationError("Invalid API key", response=response)
        elif response.status_code == 404:
            raise NotFoundError(f"Resource not found: {endpoint}", response=response)
        elif response.status_code == 422:
            raise ValidationError(
                f"Validation error: {response.text}", response=response
            )
        elif response.status_code == 429:
            raise RateLimitError("Rate limit exceeded", response=response)
        elif response.status_code >= 500:
            raise RenderError(
                f"Server error ({response.status_code}): {response.text}",
                response=response,
            )

        response.raise_for_status()
        return response.json()

    def get_asset_by_render_id(self, render_id: str) -> dict:
        """Get assets associated with a render ID.

        Args:
            render_id: The render job ID.

        Returns:
            Dict with asset information including CDN URL.
        """
        return self._request("GET", f"assets/render/{render_id}")

    def get_asset_by_id(self, asset_id: str) -> dict:
        """Get an asset by its unique asset ID.

        Args:
            asset_id: The asset ID.

        Returns:
            Dict with asset information.
        """
        return self._request("GET", f"assets/{asset_id}")
