#!/usr/bin/env python3
"""Bulk render videos from a CSV file using a template.

CSV format: title,video_url,output_name

Usage:
    export SHOTSTACK_API_KEY=your_key
    python bulk_render.py <template_id> <data.csv>
"""
import argparse
import csv
import os
import time

from dotenv import load_dotenv

from shotstack_client import MergeField, ShotstackClient, TemplateRender


def bulk_render(template_id: str, csv_path: str):
    load_dotenv()
    api_key = os.getenv("SHOTSTACK_API_KEY")
    client = ShotstackClient(api_key=api_key, environment="stage")

    results = []

    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        total = len(rows)

        for i, row in enumerate(rows, 1):
            merge_fields = [
                MergeField(find="VIDEO_URL", replace=row["video_url"]),
                MergeField(find="TITLE", replace=row["title"]),
                MergeField(find="TITLE_COLOR", replace=row.get("color", "#ffffff")),
            ]

            render_request = TemplateRender(id=template_id, merge=merge_fields)
            response = client.templates.render(render_request)

            print(f"[{i}/{total}] {row['output_name']}: {response.id} ({response.status})")
            results.append({
                "output_name": row["output_name"],
                "render_id": response.id,
                "status": response.status,
            })

            # Rate limiting - be nice to the API
            if i < total:
                time.sleep(1)

    print(f"\nCompleted: {len(results)} renders submitted")
    return results


def main():
    parser = argparse.ArgumentParser(description="Bulk render from CSV")
    parser.add_argument("template_id", help="Template ID")
    parser.add_argument("csv", help="Path to CSV file")
    args = parser.parse_args()

    bulk_render(args.template_id, args.csv)


if __name__ == "__main__":
    main()
