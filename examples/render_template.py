#!/usr/bin/env python3
"""Render a template with merge fields.

Usage:
    export SHOTSTACK_API_KEY=your_key
    python render_template.py <template_id> <title> <video_url>
"""
import argparse
import os

from dotenv import load_dotenv

from shotstack_client import MergeField, ShotstackClient, TemplateRender


def render_template(template_id: str, title: str, video_url: str, title_color: str = "#ffffff"):
    load_dotenv()
    api_key = os.getenv("SHOTSTACK_API_KEY")
    client = ShotstackClient(api_key=api_key, environment="stage")

    merge_fields = [
        MergeField(find="VIDEO_URL", replace=video_url),
        MergeField(find="TITLE", replace=title),
        MergeField(find="TITLE_COLOR", replace=title_color),
    ]

    render_request = TemplateRender(id=template_id, merge=merge_fields)
    response = client.templates.render(render_request)
    return response


def main():
    parser = argparse.ArgumentParser(description="Render a Shotstack template")
    parser.add_argument("template_id", help="Template ID")
    parser.add_argument("title", help="Title text")
    parser.add_argument("video_url", help="Video URL")
    parser.add_argument("--color", default="#ffffff", help="Title color")
    args = parser.parse_args()

    response = render_template(args.template_id, args.title, args.video_url, args.color)
    print(f"Render ID: {response.id}")
    print(f"Status: {response.status}")


if __name__ == "__main__":
    main()
