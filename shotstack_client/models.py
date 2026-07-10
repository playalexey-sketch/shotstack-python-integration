"""Data models for Shotstack API."""

from dataclasses import dataclass, field, asdict
from typing import List, Optional, Any, Dict


# --- Asset Models ---


@dataclass
class VideoAsset:
    """Video asset for use in a clip."""

    src: str
    trim: Optional[float] = None
    volume: Optional[float] = None
    volume_effect: Optional[str] = None
    crop: Optional[dict] = None

    def to_dict(self):
        d = {"type": "video", "src": self.src}
        if self.trim is not None:
            d["trim"] = self.trim
        if self.volume is not None:
            d["volume"] = self.volume
        if self.volume_effect is not None:
            d["volumeEffect"] = self.volume_effect
        if self.crop is not None:
            d["crop"] = self.crop
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "VideoAsset":
        return cls(
            src=data.get("src", ""),
            trim=data.get("trim"),
            volume=data.get("volume"),
            volume_effect=data.get("volumeEffect"),
            crop=data.get("crop"),
        )


@dataclass
class ImageAsset:
    """Image asset for use in a clip."""

    src: str
    crop: Optional[dict] = None

    def to_dict(self):
        d = {"type": "image", "src": self.src}
        if self.crop is not None:
            d["crop"] = self.crop
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "ImageAsset":
        return cls(src=data.get("src", ""), crop=data.get("crop"))


@dataclass
class AudioAsset:
    """Audio asset for use in a clip."""

    src: str
    trim: Optional[float] = None
    volume: Optional[float] = None
    effect: Optional[str] = None

    def to_dict(self):
        d = {"type": "audio", "src": self.src}
        if self.trim is not None:
            d["trim"] = self.trim
        if self.volume is not None:
            d["volume"] = self.volume
        if self.effect is not None:
            d["effect"] = self.effect
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "AudioAsset":
        return cls(
            src=data.get("src", ""),
            trim=data.get("trim"),
            volume=data.get("volume"),
            effect=data.get("effect"),
        )


@dataclass
class TitleAsset:
    """Title/text asset for use in a clip."""

    text: str
    style: Optional[str] = None
    color: Optional[str] = None
    size: Optional[str] = None
    background: Optional[str] = None
    position: Optional[str] = None
    offset: Optional[dict] = None

    def to_dict(self):
        d = {"type": "title", "text": self.text}
        if self.style is not None:
            d["style"] = self.style
        if self.color is not None:
            d["color"] = self.color
        if self.size is not None:
            d["size"] = self.size
        if self.background is not None:
            d["background"] = self.background
        if self.position is not None:
            d["position"] = self.position
        if self.offset is not None:
            d["offset"] = self.offset
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "TitleAsset":
        return cls(
            text=data.get("text", ""),
            style=data.get("style"),
            color=data.get("color"),
            size=data.get("size"),
            background=data.get("background"),
            position=data.get("position"),
            offset=data.get("offset"),
        )


@dataclass
class HtmlAsset:
    """HTML asset for use in a clip."""

    html: str
    css: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    background: Optional[str] = None

    def to_dict(self):
        d = {"type": "html", "html": self.html}
        if self.css is not None:
            d["css"] = self.css
        if self.width is not None:
            d["width"] = self.width
        if self.height is not None:
            d["height"] = self.height
        if self.background is not None:
            d["background"] = self.background
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "HtmlAsset":
        return cls(
            html=data.get("html", ""),
            css=data.get("css"),
            width=data.get("width"),
            height=data.get("height"),
            background=data.get("background"),
        )


@dataclass
class LumaAsset:
    """Luma matte asset for transitions and masks."""

    src: str
    trim: Optional[float] = None

    def to_dict(self):
        d = {"type": "luma", "src": self.src}
        if self.trim is not None:
            d["trim"] = self.trim
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "LumaAsset":
        return cls(src=data.get("src", ""), trim=data.get("trim"))


# --- Transformation Models ---


@dataclass
class RotateTransformation:
    """Rotate transformation."""

    angle: float

    def to_dict(self):
        return {"angle": self.angle}

    @classmethod
    def from_dict(cls, data: dict) -> "RotateTransformation":
        return cls(angle=data.get("angle", 0))


@dataclass
class SkewTransformation:
    """Skew transformation."""

    x: float = 0
    y: float = 0

    def to_dict(self):
        d = {}
        if self.x:
            d["x"] = self.x
        if self.y:
            d["y"] = self.y
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "SkewTransformation":
        return cls(x=data.get("x", 0), y=data.get("y", 0))


@dataclass
class FlipTransformation:
    """Flip transformation."""

    horizontal: bool = False
    vertical: bool = False

    def to_dict(self):
        d = {}
        if self.horizontal:
            d["horizontal"] = self.horizontal
        if self.vertical:
            d["vertical"] = self.vertical
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "FlipTransformation":
        return cls(
            horizontal=data.get("horizontal", False),
            vertical=data.get("vertical", False),
        )


@dataclass
class Transformation:
    """Combined transformations for a clip."""

    rotate: Optional[RotateTransformation] = None
    skew: Optional[SkewTransformation] = None
    flip: Optional[FlipTransformation] = None

    def to_dict(self):
        d = {}
        if self.rotate is not None:
            d["rotate"] = self.rotate.to_dict()
        if self.skew is not None:
            d["skew"] = self.skew.to_dict()
        if self.flip is not None:
            d["flip"] = self.flip.to_dict()
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "Transformation":
        return cls(
            rotate=RotateTransformation.from_dict(data["rotate"]) if "rotate" in data else None,
            skew=SkewTransformation.from_dict(data["skew"]) if "skew" in data else None,
            flip=FlipTransformation.from_dict(data["flip"]) if "flip" in data else None,
        )


# --- Composition Models ---


@dataclass
class Clip:
    """A clip placed on a track in the timeline."""

    asset: Any
    start: float
    length: float
    transition: Optional[dict] = None
    transform: Optional[Transformation] = None

    def to_dict(self):
        d = {
            "asset": self.asset.to_dict() if hasattr(self.asset, "to_dict") else self.asset,
            "start": self.start,
            "length": self.length,
        }
        if self.transition is not None:
            d["transition"] = self.transition
        if self.transform is not None:
            d["transform"] = self.transform.to_dict()
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "Clip":
        asset_data = data.get("asset", {})
        asset_type = asset_data.get("type", "video")
        asset_map = {
            "video": VideoAsset,
            "image": ImageAsset,
            "audio": AudioAsset,
            "title": TitleAsset,
            "html": HtmlAsset,
            "luma": LumaAsset,
        }
        asset_class = asset_map.get(asset_type, VideoAsset)
        asset = asset_class.from_dict(asset_data)
        return cls(
            asset=asset,
            start=data.get("start", 0),
            length=data.get("length", 0),
            transition=data.get("transition"),
            transform=Transformation.from_dict(data["transform"]) if "transform" in data else None,
        )


@dataclass
class Track:
    """A track containing clips in the timeline."""

    clips: List[Clip] = field(default_factory=list)

    def to_dict(self):
        return {"clips": [c.to_dict() for c in self.clips]}

    @classmethod
    def from_dict(cls, data: dict) -> "Track":
        clips = [Clip.from_dict(c) for c in data.get("clips", [])]
        return cls(clips=clips)


@dataclass
class Timeline:
    """Timeline defining the video edit structure."""

    soundtrack: Optional[str] = None
    background: Optional[str] = None
    fonts: Optional[List[dict]] = None
    tracks: List[Track] = field(default_factory=list)
    cache: bool = True

    def to_dict(self):
        d = {"tracks": [t.to_dict() for t in self.tracks], "cache": self.cache}
        if self.soundtrack is not None:
            d["soundtrack"] = self.soundtrack
        if self.background is not None:
            d["background"] = self.background
        if self.fonts is not None:
            d["fonts"] = self.fonts
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "Timeline":
        tracks = [Track.from_dict(t) for t in data.get("tracks", [])]
        return cls(
            soundtrack=data.get("soundtrack"),
            background=data.get("background"),
            fonts=data.get("fonts"),
            tracks=tracks,
            cache=data.get("cache", True),
        )


# --- Output Models ---


@dataclass
class Size:
    """Custom output size."""

    width: int
    height: int

    def to_dict(self):
        return {"width": self.width, "height": self.height}

    @classmethod
    def from_dict(cls, data: dict) -> "Size":
        return cls(width=data.get("width", 640), height=data.get("height", 480))


@dataclass
class Range:
    """Time range for rendering."""

    start: float
    length: float

    def to_dict(self):
        return {"start": self.start, "length": self.length}

    @classmethod
    def from_dict(cls, data: dict) -> "Range":
        return cls(start=data.get("start", 0), length=data.get("length", 0))


@dataclass
class Poster:
    """Poster image configuration."""

    capture: float

    def to_dict(self):
        return {"capture": self.capture}

    @classmethod
    def from_dict(cls, data: dict) -> "Poster":
        return cls(capture=data.get("capture", 0))


@dataclass
class Thumbnail:
    """Thumbnail image configuration."""

    capture: float
    scale: float

    def to_dict(self):
        return {"capture": self.capture, "scale": self.scale}

    @classmethod
    def from_dict(cls, data: dict) -> "Thumbnail":
        return cls(capture=data.get("capture", 0), scale=data.get("scale", 0.3))


# --- Destination Models ---


@dataclass
class ShotstackDestination:
    """Default Shotstack hosting destination."""

    provider: str = "shotstack"
    exclude: bool = False

    def to_dict(self):
        d = {"provider": self.provider}
        if self.exclude:
            d["exclude"] = self.exclude
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "ShotstackDestination":
        return cls(provider=data.get("provider", "shotstack"), exclude=data.get("exclude", False))


@dataclass
class S3Destination:
    """S3 upload destination."""

    provider: str = "s3"
    options: Optional[dict] = None

    def to_dict(self):
        d = {"provider": self.provider}
        if self.options is not None:
            d["options"] = self.options
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "S3Destination":
        return cls(provider="s3", options=data.get("options"))


@dataclass
class MuxDestination:
    """Mux video hosting destination."""

    provider: str = "mux"
    options: Optional[dict] = None

    def to_dict(self):
        d = {"provider": self.provider}
        if self.options is not None:
            d["options"] = self.options
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "MuxDestination":
        return cls(provider="mux", options=data.get("options"))


@dataclass
class Output:
    """Output configuration for rendered video."""

    format: str = "mp4"
    resolution: str = "sd"
    size: Optional[Size] = None
    fps: Optional[float] = None
    quality: Optional[str] = None
    range: Optional[Range] = None
    poster: Optional[Poster] = None
    thumbnail: Optional[Thumbnail] = None
    destinations: Optional[List[Any]] = None

    def to_dict(self):
        d = {"format": self.format, "resolution": self.resolution}
        if self.size is not None:
            d["size"] = self.size.to_dict()
        if self.fps is not None:
            d["fps"] = self.fps
        if self.quality is not None:
            d["quality"] = self.quality
        if self.range is not None:
            d["range"] = self.range.to_dict()
        if self.poster is not None:
            d["poster"] = self.poster.to_dict()
        if self.thumbnail is not None:
            d["thumbnail"] = self.thumbnail.to_dict()
        if self.destinations is not None:
            d["destinations"] = [
                dest.to_dict() if hasattr(dest, "to_dict") else dest for dest in self.destinations
            ]
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "Output":
        return cls(
            format=data.get("format", "mp4"),
            resolution=data.get("resolution", "sd"),
            size=Size.from_dict(data["size"]) if "size" in data else None,
            fps=data.get("fps"),
            quality=data.get("quality"),
            range=Range.from_dict(data["range"]) if "range" in data else None,
            poster=Poster.from_dict(data["poster"]) if "poster" in data else None,
            thumbnail=Thumbnail.from_dict(data["thumbnail"]) if "thumbnail" in data else None,
            destinations=data.get("destinations"),
        )


# --- Edit & Template Models ---


@dataclass
class Edit:
    """Main edit object sent to the API for rendering."""

    timeline: Timeline
    output: Output
    merge: Optional[List[Any]] = None
    callback: Optional[str] = None

    def to_dict(self):
        d = {"timeline": self.timeline.to_dict(), "output": self.output.to_dict()}
        if self.merge is not None:
            d["merge"] = [m.to_dict() for m in self.merge]
        if self.callback is not None:
            d["callback"] = self.callback
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "Edit":
        return cls(
            timeline=Timeline.from_dict(data.get("timeline", {})),
            output=Output.from_dict(data.get("output", {})),
            merge=[MergeField.from_dict(m) for m in data["merge"]] if "merge" in data else None,
            callback=data.get("callback"),
        )


@dataclass
class MergeField:
    """Merge field for template placeholders."""

    find: str
    replace: Any

    def to_dict(self):
        return {"find": self.find, "replace": self.replace}

    @classmethod
    def from_dict(cls, data: dict) -> "MergeField":
        return cls(find=data.get("find", ""), replace=data.get("replace"))


@dataclass
class Template:
    """Template for reusable video edits."""

    name: str
    template: Edit

    def to_dict(self):
        return {"name": self.name, "template": self.template.to_dict()}

    @classmethod
    def from_dict(cls, data: dict) -> "Template":
        return cls(
            name=data.get("name", ""),
            template=Edit.from_dict(data.get("template", {})),
        )


@dataclass
class TemplateRender:
    """Request to render a template with merge fields."""

    id: str
    merge: Optional[List[MergeField]] = None

    def to_dict(self):
        d = {"id": self.id}
        if self.merge is not None:
            d["merge"] = [m.to_dict() for m in self.merge]
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "TemplateRender":
        return cls(
            id=data.get("id", ""),
            merge=[MergeField.from_dict(m) for m in data["merge"]] if "merge" in data else None,
        )


# --- Response Models ---


@dataclass
class RenderResponse:
    """Response from a render request."""

    id: Optional[str] = None
    status: Optional[str] = None
    url: Optional[str] = None
    error: Optional[str] = None

    def is_done(self) -> bool:
        return self.status == "done"

    def is_failed(self) -> bool:
        return self.status in ("failed", "error")

    def is_pending(self) -> bool:
        return self.status in ("queued", "processing", "pending")

    def to_dict(self):
        d = {}
        if self.id is not None:
            d["id"] = self.id
        if self.status is not None:
            d["status"] = self.status
        if self.url is not None:
            d["url"] = self.url
        if self.error is not None:
            d["error"] = self.error
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "RenderResponse":
        return cls(
            id=data.get("id"),
            status=data.get("status"),
            url=data.get("url"),
            error=data.get("error"),
        )
