"""Shotstack Python Integration - Cloud Video Editing API Client."""

from .client import ShotstackClient
from .config import ShotstackConfig
from .models import (
    VideoAsset,
    ImageAsset,
    AudioAsset,
    TitleAsset,
    HtmlAsset,
    LumaAsset,
    Clip,
    Track,
    Timeline,
    Output,
    Edit,
    Template,
    TemplateRender,
    MergeField,
    RenderResponse,
    Size,
    Range,
    Poster,
    Thumbnail,
    ShotstackDestination,
    S3Destination,
    MuxDestination,
    Transformation,
    RotateTransformation,
    SkewTransformation,
    FlipTransformation,
)
from .exceptions import (
    ShotstackError,
    AuthenticationError,
    RenderError,
    NotFoundError,
    ValidationError,
    RateLimitError,
)

__version__ = "0.1.0"
__all__ = ["ShotstackClient", "ShotstackConfig"]