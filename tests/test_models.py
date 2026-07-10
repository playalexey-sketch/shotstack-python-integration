"""Tests for Shotstack data models."""

import pytest

from shotstack_client.models import (
    Clip,
    Edit,
    ImageAsset,
    MergeField,
    Output,
    Range,
    RenderResponse,
    Size,
    Template,
    TemplateRender,
    Timeline,
    TitleAsset,
    Track,
    VideoAsset,
)


class TestVideoAsset:
    """Test VideoAsset model."""

    def test_to_dict(self):
        asset = VideoAsset(src="https://example.com/video.mp4", trim=5.0, volume=0.8)
        d = asset.to_dict()
        assert d["type"] == "video"
        assert d["src"] == "https://example.com/video.mp4"
        assert d["trim"] == 5.0
        assert d["volume"] == 0.8

    def test_to_dict_minimal(self):
        asset = VideoAsset(src="https://example.com/video.mp4")
        d = asset.to_dict()
        assert d == {"type": "video", "src": "https://example.com/video.mp4"}

    def test_from_dict(self):
        asset = VideoAsset.from_dict(
            {"src": "https://example.com/video.mp4", "trim": 3.0}
        )
        assert asset.src == "https://example.com/video.mp4"
        assert asset.trim == 3.0


class TestClip:
    """Test Clip model."""

    def test_serialization(self):
        video = VideoAsset(src="https://example.com/v.mp4")
        clip = Clip(asset=video, start=0.0, length=5.0)
        d = clip.to_dict()
        assert d["start"] == 0.0
        assert d["length"] == 5.0
        assert d["asset"]["src"] == "https://example.com/v.mp4"

    def test_with_title_asset(self):
        title = TitleAsset(text="Hello", color="#ffffff")
        clip = Clip(asset=title, start=1.0, length=3.0)
        d = clip.to_dict()
        assert d["asset"]["type"] == "title"
        assert d["asset"]["text"] == "Hello"


class TestTimeline:
    """Test Timeline model."""

    def test_with_multiple_tracks(self):
        video = VideoAsset(src="https://example.com/v.mp4")
        title = TitleAsset(text="Overlay")
        track1 = Track(clips=[Clip(asset=video, start=0.0, length=10.0)])
        track2 = Track(clips=[Clip(asset=title, start=0.0, length=10.0)])
        timeline = Timeline(tracks=[track1, track2])
        d = timeline.to_dict()
        assert len(d["tracks"]) == 2
        assert d["cache"] is True


class TestEdit:
    """Test Edit model."""

    def test_full_serialization(self):
        video = VideoAsset(src="https://example.com/v.mp4")
        clip = Clip(asset=video, start=0.0, length=5.0)
        track = Track(clips=[clip])
        timeline = Timeline(tracks=[track])
        output = Output(format="mp4", resolution="sd")
        edit = Edit(timeline=timeline, output=output)
        d = edit.to_dict()
        assert "timeline" in d
        assert "output" in d
        assert d["output"]["format"] == "mp4"


class TestMergeField:
    """Test MergeField model."""

    def test_to_dict(self):
        mf = MergeField(find="TITLE", replace="Hello")
        assert mf.to_dict() == {"find": "TITLE", "replace": "Hello"}

    def test_from_dict(self):
        mf = MergeField.from_dict({"find": "URL", "replace": "https://example.com"})
        assert mf.find == "URL"
        assert mf.replace == "https://example.com"


class TestRenderResponse:
    """Test RenderResponse model."""

    def test_from_dict(self):
        resp = RenderResponse.from_dict(
            {"id": "abc123", "status": "done", "url": "https://cdn.example.com/v.mp4"}
        )
        assert resp.id == "abc123"
        assert resp.status == "done"
        assert resp.url == "https://cdn.example.com/v.mp4"

    def test_status_helpers(self):
        done = RenderResponse(status="done")
        pending = RenderResponse(status="queued")
        failed = RenderResponse(status="failed")
        assert done.is_done() is True
        assert pending.is_pending() is True
        assert failed.is_failed() is True

    def test_to_dict(self):
        resp = RenderResponse(id="x", status="processing")
        d = resp.to_dict()
        assert d == {"id": "x", "status": "processing"}


class TestTemplateRender:
    """Test TemplateRender model."""

    def test_with_merge_fields(self):
        tr = TemplateRender(
            id="template123",
            merge=[MergeField(find="TITLE", replace="Hello")],
        )
        d = tr.to_dict()
        assert d["id"] == "template123"
        assert d["merge"][0]["find"] == "TITLE"
