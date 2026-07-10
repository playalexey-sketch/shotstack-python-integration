"""Tests for ShotstackClient."""

import os
from unittest.mock import patch

import pytest

from shotstack_client import ShotstackClient
from shotstack_client.config import ShotstackConfig
from shotstack_client.edit_api import EditAPI
from shotstack_client.serve_api import ServeAPI
from shotstack_client.template_api import TemplateAPI


class TestShotstackClient:
    """Test suite for ShotstackClient."""

    def test_init_with_api_key(self):
        """Test client initialization with explicit API key."""
        client = ShotstackClient(api_key="test_key", environment="stage")
        assert client.config.api_key == "test_key"
        assert client.config.environment == "stage"

    def test_init_from_env(self):
        """Test client initialization from environment variable."""
        with patch.dict(os.environ, {"SHOTSTACK_API_KEY": "env_key"}):
            client = ShotstackClient(environment="stage")
            assert client.config.api_key == "env_key"

    def test_init_without_key_raises(self):
        """Test that ValueError is raised without API key."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError):
                ShotstackClient()

    def test_environment_selection_stage(self):
        """Test stage environment URL."""
        client = ShotstackClient(api_key="key", environment="stage")
        assert client.config.base_url == "https://api.shotstack.io/stage"

    def test_environment_selection_production(self):
        """Test production environment URL."""
        client = ShotstackClient(api_key="key", environment="production")
        assert client.config.base_url == "https://api.shotstack.io/v1"

    def test_invalid_environment_raises(self):
        """Test that invalid environment raises ValueError."""
        with pytest.raises(ValueError):
            ShotstackClient(api_key="key", environment="invalid")

    def test_client_properties(self):
        """Test that client exposes edit, templates, and serve APIs."""
        client = ShotstackClient(api_key="key")
        assert isinstance(client.edit, EditAPI)
        assert isinstance(client.templates, TemplateAPI)
        assert isinstance(client.serve, ServeAPI)
