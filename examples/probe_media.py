#!/usr/bin/env python3
"""Probe a media file for metadata.

Usage:
    export SHOTSTACK_API_KEY=your_key
    python probe_media.py <media_url>
"""
import argparse
import os

from dotenv import load_dotenv

from shotstack_client import ShotstackClient


def probe(url: str):
    load_dotenv()
    api_key = os.getenv("SHOTSTACK_API_KEY")
    client = ShotstackClient(api_key=api_key, environment="stage")

    result = client.edit.probe_media(url)
    metadata = result.get("metadata", {})
    format_info = metadata.get("format", {})
    streams = metadata.get("streams", [])

    print(f"File: {format_info.get('filename', url)}")
    print(f"Format: {format_info.get('format_name', 'unknown')}")
    print(f"Duration: {format_info.get('duration', 'unknown')}s")
    print(f"Bitrate: {format_info.get('bit_rate', 'unknown')}")
    print("-" * 40)

    for stream in streams:
        codec_type = stream.get("codec_type", "unknown")
        print(f"\nStream: {codec_type}")
        print(f"  Codec: {stream.get('codec_name', 'unknown')}")
        if codec_type == "video":
            print(f"  Width: {stream.get('width')}px")
            print(f"  Height: {stream.get('height')}px")
            print(f"  FPS: {stream.get('r_frame_rate')}")
        elif codec_type == "audio":
            print(f"  Sample rate: {stream.get('sample_rate')}Hz")
            print(f"  Channels: {stream.get('channels')}")


def main():
    parser = argparse.ArgumentParser(description="Probe media file metadata")
    parser.add_argument("url", help="Publicly accessible media URL")
    args = parser.parse_args()

    probe(args.url)


if __name__ == "__main__":
    main()
