#!/usr/bin/env python3
"""Basic video editing example - trim and render a video clip.

Usage:
    export SHOTSTACK_API_KEY=your_key
    python video_edit.py
"""
import os

from dotenv import load_dotenv

from shotstack_client import (
    Clip,
    Edit,
    Output,
    ShotstackClient,
    Timeline,
    Track,
    VideoAsset,
)


def main():
    load_dotenv()
    api_key = os.getenv("SHOTSTACK_API_KEY")
    if not api_key:
        raise ValueError("Set SHOTSTACK_API_KEY environment variable")

    client = ShotstackClient(api_key=api_key, environment="stage")

    # Create a video asset with trim
    video = VideoAsset(
        src="https://shotstack-assets.s3.amazonaws.com/footage/skater.mp4",
        trim=3.0,
    )

    # Place the video on a clip (8 seconds long, starting at 0)
    clip = Clip(asset=video, start=0.0, length=8.0)

    # Add clip to a track
    track = Track(clips=[clip])

    # Build timeline and output
    timeline = Timeline(tracks=[track])
    output = Output(format="mp4", resolution="sd")
    edit = Edit(timeline=timeline, output=output)

    # Submit render
    response = client.edit.render(edit)
    print(f"Render ID: {response.id}")
    print(f"Status: {response.status}")
    print(f"Poll for status: python check_status.py {response.id}")


if __name__ == "__main__":
    main()
