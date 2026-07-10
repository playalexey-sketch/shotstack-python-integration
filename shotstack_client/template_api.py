"""Template API for Shotstack template operations."""

from typing import List, Optional

from .config import ShotstackConfig
from .models import RenderResponse, Template, TemplateRender


class TemplateAPI:
    """API client for template CRUD and rendering operations."""

    def __init__(self, config: ShotstackConfig):
        self.config = config
        self._edit_api = None

    def _request(self, method: str, endpoint: str, data: Optional[dict] = None) -> dict:
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

    def create(self, template: Template) -> dict:
        """Create a new template.

        Args:
            template: Template object to save.

        Returns:
            API response dict with template ID.
        """
        data = template.to_dict()
        return self._request("POST", "template", data)

    def list(self) -> List[dict]:
        """List all templates.

        Returns:
            List of template dicts.
        """
        result = self._request("GET", "template")
        return result.get("data", [])

    def get(self, template_id: str) -> dict:
        """Get a template by ID.

        Args:
            template_id: Template ID.

        Returns:
            Template dict.
        """
        return self._request("GET", f"template/{template_id}")

    def render(self, render_request: TemplateRender) -> RenderResponse:
        """Render a template with merge fields.

        Args:
            render_request: TemplateRender with template ID and merge fields.

        Returns:
            RenderResponse with render ID and status.
        """
        data = render_request.to_dict()
        result = self._request("POST", "template/render", data)
        response_data = result.get("response", {})
        return RenderResponse(
            id=response_data.get("id"),
            status=response_data.get("status"),
            url=response_data.get("url"),
            error=response_data.get("error"),
        )

    def delete(self, template_id: str) -> bool:
        """Delete a template.

        Args:
            template_id: Template ID to delete.

        Returns:
            True if deleted successfully.
        """
        self._request("DELETE", f"template/{template_id}")
        return True
