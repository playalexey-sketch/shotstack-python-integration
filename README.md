# Shotstack Python Integration

Python client library for [Shotstack](https://shotstack.io/) Cloud Video Editing API. Create, edit, and render videos programmatically with a clean, Pythonic interface.

## Features

- **Video Editing** - Programmatic video creation with clips, transitions, effects
- **Text Overlays** - Add styled titles and text to videos
- **Image Sequences** - Create slideshows and image-based videos
- **Templates** - Save and reuse video templates with merge fields
- **Media Inspection** - Probe media files for metadata
- **Asset Management** - Manage rendered assets and CDN URLs
- **Async Support** - Poll render status with built-in helpers

## Installation

```bash
pip install -r requirements.txt
```

For development:

```bash
pip install -r requirements-dev.txt
```

## Quick Start

1. Get your API key from [Shotstack Dashboard](https://dashboard.shotstack.io/)
2. Set environment variables:

```bash
export SHOTSTACK_API_KEY=your_key_here
export SHOTSTACK_ENV=stage  # or 'production'
```

3. Render your first video:

```python
from shotstack_client import (
    ShotstackClient, VideoAsset, Clip, Track, Timeline, Output, Edit
)

client = ShotstackClient(api_key="your_api_key")

video = VideoAsset(
    src="https://example.com/video.mp4",
    trim=3.0
)
clip = Clip(asset=video, start=0.0, length=8.0)
track = Track(clips=[clip])
timeline = Timeline(tracks=[track])
output = Output(format="mp4", resolution="sd")
edit = Edit(timeline=timeline, output=output)

response = client.edit.render(edit)
print(f"Render ID: {response.id}")
```

## Examples

| Example | Description |
|---------|-------------|
| `video_edit.py` | Basic video trimming and rendering |
| `text_overlay.py` | Add text titles over video |
| `images_to_video.py` | Create slideshow from images |
| `create_template.py` | Save video as reusable template |
| `render_template.py` | Render template with merge fields |
| `check_status.py` | Poll render status |
| `probe_media.py` | Inspect media metadata |
| `bulk_render.py` | Batch render from CSV |

## API Overview

### ShotstackClient

Main entry point providing access to all API sections:

```python
client = ShotstackClient(api_key="your_key", environment="stage")

# Video editing
client.edit.render(edit)
client.edit.get_render_status(render_id)
client.edit.probe_media(url)

# Templates
client.templates.create(template)
client.templates.list()
client.templates.get(template_id)
client.templates.render(template_render)
client.templates.delete(template_id)

# Assets
client.serve.get_asset_by_render_id(render_id)
client.serve.get_asset_by_id(asset_id)
```

## Project Structure

```
shotstack-integration/
├── shotstack_client/      # Core client package
│   ├── client.py          # Main client
│   ├── config.py          # Configuration
│   ├── models.py          # Data models
│   ├── edit_api.py        # Video editing API
│   ├── template_api.py    # Template API
│   ├── serve_api.py       # Asset management API
│   └── exceptions.py      # Custom exceptions
├── examples/              # Usage examples
├── tests/                 # Unit tests
├── .github/workflows/     # CI/CD
└── requirements.txt       # Dependencies
```

## CI/CD

GitHub Actions workflow runs on every push and PR:
- Python 3.8-3.11 matrix testing
- Linting with flake8
- Format checking with black
- Type checking with mypy
- Test coverage with pytest-cov

## License

MIT License - see [LICENSE](LICENSE) file.
