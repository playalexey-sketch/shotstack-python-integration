#!/usr/bin/env python3
"""Create a slideshow video from a list of image URLs.

Usage:
    export SHOTSTACK_API_KEY=your_key
    python images_to_video.py https://example.com/img1.jpg https://example.com/img2.jpg
"""
import argparse
import os

from dotenv import load_dotenv

from shotstack_client import (
    AudioAsset,
    Clip,
    Edit,
    ImageAsset,
    Output,
    ShotstackClient,
    Timeline,
    Track,
)


def create_slideshow(image_urls, soundtrack_url=None):
    load_dotenv()
    api_key = os.getenv("SHOTSTACK_API_KEY")
    client = ShotstackClient(api_key=api_key, environment="stage")

    clips = []
    for i, url in enumerate(image_urls):
        image = ImageAsset(src=url)
        clip = Clip(
            asset=image,
            start=i * 3.0,
            length=3.0,
            transition={"in": "fade", "out": "fade"},
        )
        clips.append(clip)

    tracks = [Track(clips=clips)]

    # Optional soundtrack
    if soundtrack_url:
        audio = AudioAsset(src=soundtrack_url, volume=0.5, effect="fadeInFadeOut")
        audio_clip = Clip(
            asset=audio,
            start=0.0,
            length=len(image_urls) * 3.0,
        )
        tracks.append(Track(clips=[audio_clip]))

    timeline = Timeline(tracks=tracks)
    output = Output(format="mp4", resolution="sd")
    edit = Edit(timeline=timeline, output=output)

    response = client.edit.render(edit)
    return response


def main():
    parser = argparse.ArgumentParser(description="Create slideshow from images")
    parser.add_argument("images", nargs="+", help="Image URLs")
    parser.add_argument("--soundtrack", "-s", help="Soundtrack URL")
    args = parser.parse_args()

    response = create_slideshow(args.images, args.soundtrack)
    print(f"Render ID: {response.id}")
    print(f"Status: {response.status}")


if __name__ == "__main__":
    main()
