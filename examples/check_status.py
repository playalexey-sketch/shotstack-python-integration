#!/usr/bin/env python3
"""Poll render status until complete.

Usage:
    export SHOTSTACK_API_KEY=your_key
    python check_status.py <render_id>
"""
import argparse
import os
import sys
import time

from dotenv import load_dotenv

from shotstack_client import ShotstackClient


def poll_status(render_id: str, interval: int = 10):
    load_dotenv()
    api_key = os.getenv("SHOTSTACK_API_KEY")
    client = ShotstackClient(api_key=api_key, environment="stage")

    print(f"Polling render {render_id} every {interval}s...")
    print("-" * 40)

    while True:
        response = client.edit.get_render_status(render_id)
        print(f"Status: {response.status}")

        if response.is_done():
            print(f"\nDone! Video URL: {response.url}")
            return response
        elif response.is_failed():
            print(f"\nRender failed: {response.error}")
            sys.exit(1)

        time.sleep(interval)


def main():
    parser = argparse.ArgumentParser(description="Check render status")
    parser.add_argument("render_id", help="Render job ID")
    parser.add_argument("--interval", type=int, default=10, help="Polling interval in seconds")
    args = parser.parse_args()

    poll_status(args.render_id, args.interval)


if __name__ == "__main__":
    main()
