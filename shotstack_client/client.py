"""Main Shotstack API client."""

import os

from .config import ShotstackConfig
from .edit_api import EditAPI
from .exceptions import ShotstackError
from .serve_api import ServeAPI
from .template_api import TemplateAPI


class ShotstackClient:
    """Main client for Shotstack Cloud Video Editing API.

    Provides access to video editing, template management, and asset
    operations through dedicated sub-APIs.

    Args:
        api_key: Shotstack API key. Falls back to SHOTSTACK_API_KEY env var.
        environment: API environment - 'stage' (default) or 'production'.

    Example:
        client = ShotstackClient(api_key="your_key")
        response = client.edit.render(edit)
    """

    def __init__(self, api_key: str = None, environment: str = "stage"):
        if not api_key:
            api_key = os.environ.get("SHOTSTACK_API_KEY")
        if not api_key:
            raise ValueError(
                "API key is required. Set SHOTSTACK_API_KEY environment variable "
                "or pass api_key parameter."
            )
        self.config = ShotstackConfig(api_key=api_key, environment=environment)
        self._edit = EditAPI(self.config)
        self._templates = TemplateAPI(self.config)
        self._serve = ServeAPI(self.config)

    @property
    def edit(self) -> EditAPI:
        """Video editing API."""
        return self._edit

    @property
    def templates(self) -> TemplateAPI:
        """Template management API."""
        return self._templates

    @property
    def serve(self) -> ServeAPI:
        """Asset management API."""
        return self._serve
