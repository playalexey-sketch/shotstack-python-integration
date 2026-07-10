#!/usr/bin/env python3
"""Create a reusable video template with placeholders.

Usage:
    export SHOTSTACK_API_KEY=your_key
    python create_template.py
"""
import os

from dotenv import load_dotenv

from shotstack_client import (
    Clip,
    Edit,
    Output,
    ShotstackClient,
    Template,
    Timeline,
    TitleAsset,
    Track,
    VideoAsset,
)


def main():
    load_dotenv()
    api_key = os.getenv("SHOTSTACK_API_KEY")
    if not api_key:
        raise ValueError("Set SHOTSTACK_API_KEY environment variable")

    client = ShotstackClient(api_key=api_key, environment="stage")

    # Create template with placeholders
    video = VideoAsset(src="{{ VIDEO_URL }}")
    video_clip = Clip(asset=video, start=0.0, length=10.0)

    title = TitleAsset(
        text="{{ TITLE }}",
        style="minimal",
        color="{{ TITLE_COLOR }}",
        size="large",
        position="center",
    )
    title_clip = Clip(asset=title, start=0.0, length=10.0)

    track1 = Track(clips=[video_clip])
    track2 = Track(clips=[title_clip])

    timeline = Timeline(tracks=[track1, track2])
    output = Output(format="mp4", resolution="sd")
    edit = Edit(timeline=timeline, output=output)

    template = Template(name="My Video Template", template=edit)

    result = client.templates.create(template)
    template_id = result.get("response", {}).get("id")
    print(f"Template created with ID: {template_id}")


if __name__ == "__main__":
    main()
