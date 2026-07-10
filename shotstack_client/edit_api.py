"""Edit API for Shotstack video rendering operations."""

import json
import time
from typing import Optional

import requests

from .config import ShotstackConfig
from .exceptions import (
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    RenderError,
    ValidationError,
)
from .models import Edit, RenderResponse


class EditAPI:
    """API client for video editing and rendering operations."""

    def __init__(self, config: ShotstackConfig):
        self.config = config

    def _request(self, method: str, endpoint: str, data: Optional[dict] = None) -> dict:
        """Make an HTTP request to the Shotstack API.

        Args:
            method: HTTP method (GET, POST, DELETE).
            endpoint: API endpoint path.
            data: Optional request body data.

        Returns:
            Parsed JSON response as dict.

        Raises:
            AuthenticationError: On 401 response.
            NotFoundError: On 404 response.
            ValidationError: On 422 response.
            RateLimitError: On 429 response.
            RenderError: On 5xx response.
        """
        url = f"{self.config.base_url}/{endpoint}"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.config.api_key,
        }

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=data,
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

    def render(self, edit: Edit) -> RenderResponse:
        """Submit a video edit for rendering.

        Args:
            edit: Edit object defining the video timeline and output.

        Returns:
            RenderResponse with render ID and initial status.
        """
        data = edit.to_dict()
        result = self._request("POST", "render", data)
        response_data = result.get("response", {})
        return RenderResponse(
            id=response_data.get("id"),
            status=response_data.get("status"),
            url=response_data.get("url"),
            error=response_data.get("error"),
        )

    def get_render_status(self, render_id: str) -> RenderResponse:
        """Get the status of a render job.

        Args:
            render_id: The ID of the render job.

        Returns:
            RenderResponse with current status and URL if done.
        """
        result = self._request("GET", f"render/{render_id}")
        response_data = result.get("response", {})
        return RenderResponse(
            id=response_data.get("id"),
            status=response_data.get("status"),
            url=response_data.get("url"),
            error=response_data.get("error"),
        )

    def probe_media(self, url: str) -> dict:
        """Probe a media file for metadata.

        Args:
            url: Publicly accessible URL of the media file.

        Returns:
            Dict with media metadata (width, height, duration, etc.).
        """
        result = self._request("GET", f"probe?url={url}")
        return result.get("response", {})

    def poll_until_done(
        self, render_id: str, interval: int = 10, timeout: int = 300
    ) -> RenderResponse:
        """Poll render status until done or failed.

        Args:
            render_id: The ID of the render job.
            interval: Polling interval in seconds.
            timeout: Maximum time to wait in seconds.

        Returns:
            Final RenderResponse.

        Raises:
            RenderError: If polling times out or render fails.
        """
        start = time.time()
        while time.time() - start < timeout:
            response = self.get_render_status(render_id)
            if response.is_done():
                return response
            if response.is_failed():
                raise RenderError(
                    f"Render failed: {response.error}",
                    response=response.to_dict(),
                )
            time.sleep(interval)
        raise RenderError("Render polling timed out")
