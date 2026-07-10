#!/usr/bin/env python3
"""Text overlay example - add animated title over video.

Usage:
    export SHOTSTACK_API_KEY=your_key
    python text_overlay.py
"""
import os

from dotenv import load_dotenv

from shotstack_client import (
    AudioAsset,
    Clip,
    Edit,
    Output,
    ShotstackClient,
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

    # Background video
    video = VideoAsset(
        src="https://shotstack-assets.s3.amazonaws.com/footage/skater.mp4",
        trim=5.0,
    )
    video_clip = Clip(asset=video, start=0.0, length=10.0)

    # Title overlay
    title = TitleAsset(
        text="Hello World!",
        style="minimal",
        color="#ffffff",
        size="large",
        position="center",
    )
    title_clip = Clip(asset=title, start=0.0, length=10.0)

    # Soundtrack
    soundtrack = AudioAsset(
        src="https://shotstack-assets.s3.amazonaws.com/music/unminus/lit.mp3",
        volume=0.3,
        effect="fadeInFadeOut",
    )
    audio_clip = Clip(asset=soundtrack, start=0.0, length=10.0)

    # Layer: video on bottom, title on top, audio mixed in
    video_track = Track(clips=[video_clip])
    title_track = Track(clips=[title_clip])
    audio_track = Track(clips=[audio_clip])

    timeline = Timeline(tracks=[video_track, title_track, audio_track])
    output = Output(format="mp4", resolution="sd")
    edit = Edit(timeline=timeline, output=output)

    response = client.edit.render(edit)
    print(f"Render ID: {response.id}")
    print(f"Status: {response.status}")


if __name__ == "__main__":
    main()
