from __future__ import annotations

import csv
from pathlib import Path

from pin_generator.models import ImageAsset, PinRecord


PINTEREST_HEADERS = [
    "Title",
    "Media URL",
    "Pinterest board",
    "Thumbnail",
    "Description",
    "Link",
    "Publish date",
    "Keywords",
]


def save_pinterest_csv(records: list[PinRecord], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=PINTEREST_HEADERS)
        writer.writeheader()
        for r in records:
            writer.writerow(
                {
                    "Title": r.title,
                    "Media URL": r.media_url,
                    "Pinterest board": r.pinterest_board,
                    "Thumbnail": r.thumbnail,
                    "Description": r.description,
                    "Link": r.link,
                    "Publish date": r.publish_date,
                    "Keywords": r.keywords,
                }
            )


def save_upload_manifest(assets: list[ImageAsset], media_base_url: str, output_path: Path) -> None:
    """Helper file showing how local files map to expected public URLs."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["local_path", "suggested_public_url"])
        writer.writeheader()
        for asset in assets:
            writer.writerow(
                {
                    "local_path": str(asset.local_path),
                    "suggested_public_url": f"{media_base_url.rstrip('/')}/{asset.local_path.name}",
                }
            )
