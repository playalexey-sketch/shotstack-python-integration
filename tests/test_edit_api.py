"""Tests for EditAPI."""

import pytest
import responses

from shotstack_client import (
    Clip,
    Edit,
    Output,
    Timeline,
    Track,
    VideoAsset,
)
from shotstack_client.config import ShotstackConfig
from shotstack_client.edit_api import EditAPI
from shotstack_client.exceptions import (
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    RenderError,
    ValidationError,
)

API_KEY = "test_api_key"
BASE_URL = "https://api.shotstack.io/stage"


class TestEditAPI:
    """Test suite for EditAPI."""

    @pytest.fixture
    def api(self):
        config = ShotstackConfig(api_key=API_KEY, environment="stage")
        return EditAPI(config)

    @responses.activate
    def test_render_success(self, api):
        """Test successful render submission."""
        responses.add(
            responses.POST,
            f"{BASE_URL}/render",
            json={"response": {"id": "abc123", "status": "queued"}},
            status=201,
        )

        video = VideoAsset(src="https://example.com/video.mp4")
        clip = Clip(asset=video, start=0.0, length=5.0)
        edit = Edit(timeline=Timeline(tracks=[Track(clips=[clip])]), output=Output())

        response = api.render(edit)
        assert response.id == "abc123"
        assert response.status == "queued"

    @responses.activate
    def test_render_authentication_error(self, api):
        """Test 401 authentication error."""
        responses.add(
            responses.POST,
            f"{BASE_URL}/render",
            json={"error": "Unauthorized"},
            status=401,
        )

        video = VideoAsset(src="https://example.com/video.mp4")
        clip = Clip(asset=video, start=0.0, length=5.0)
        edit = Edit(timeline=Timeline(tracks=[Track(clips=[clip])]), output=Output())

        with pytest.raises(AuthenticationError):
            api.render(edit)

    @responses.activate
    def test_render_validation_error(self, api):
        """Test 422 validation error."""
        responses.add(
            responses.POST,
            f"{BASE_URL}/render",
            json={"error": "Invalid input"},
            status=422,
        )

        video = VideoAsset(src="https://example.com/video.mp4")
        clip = Clip(asset=video, start=0.0, length=5.0)
        edit = Edit(timeline=Timeline(tracks=[Track(clips=[clip])]), output=Output())

        with pytest.raises(ValidationError):
            api.render(edit)

    @responses.activate
    def test_render_rate_limit_error(self, api):
        """Test 429 rate limit error."""
        responses.add(
            responses.POST,
            f"{BASE_URL}/render",
            json={"error": "Rate limited"},
            status=429,
        )

        video = VideoAsset(src="https://example.com/video.mp4")
        clip = Clip(asset=video, start=0.0, length=5.0)
        edit = Edit(timeline=Timeline(tracks=[Track(clips=[clip])]), output=Output())

        with pytest.raises(RateLimitError):
            api.render(edit)

    @responses.activate
    def test_render_server_error(self, api):
        """Test 500 server error."""
        responses.add(
            responses.POST,
            f"{BASE_URL}/render",
            json={"error": "Internal error"},
            status=500,
        )

        video = VideoAsset(src="https://example.com/video.mp4")
        clip = Clip(asset=video, start=0.0, length=5.0)
        edit = Edit(timeline=Timeline(tracks=[Track(clips=[clip])]), output=Output())

        with pytest.raises(RenderError):
            api.render(edit)

    @responses.activate
    def test_get_render_status(self, api):
        """Test getting render status."""
        responses.add(
            responses.GET,
            f"{BASE_URL}/render/abc123",
            json={"response": {"id": "abc123", "status": "done", "url": "https://cdn.example.com/v.mp4"}},
            status=200,
        )

        response = api.get_render_status("abc123")
        assert response.id == "abc123"
        assert response.status == "done"
        assert response.url == "https://cdn.example.com/v.mp4"

    @responses.activate
    def test_probe_media(self, api):
        """Test media probing."""
        responses.add(
            responses.GET,
            f"{BASE_URL}/probe",
            json={"response": {"metadata": {"streams": [{"codec_type": "video", "width": 1920, "height": 1080}]}}},
            status=200,
        )

        result = api.probe_media("https://example.com/video.mp4")
        assert "metadata" in result

    @responses.activate
    def test_render_not_found_error(self, api):
        """Test 404 not found error."""
        responses.add(
            responses.GET,
            f"{BASE_URL}/render/missing",
            json={"error": "Not found"},
            status=404,
        )

        with pytest.raises(NotFoundError):
            api.get_render_status("missing")
