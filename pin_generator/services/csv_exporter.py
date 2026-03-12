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


def _pin_record_to_row(record: PinRecord) -> dict[str, str]:
    return {
        "Title": record.title,
        "Media URL": record.media_url,
        "Pinterest board": record.pinterest_board,
        "Thumbnail": record.thumbnail,
        "Description": record.description,
        "Link": record.link,
        "Publish date": record.publish_date,
        "Keywords": record.keywords,
    }


def save_pinterest_csv(records: list[PinRecord], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=PINTEREST_HEADERS)
        writer.writeheader()
        for r in records:
            writer.writerow(_pin_record_to_row(r))


def save_pinterest_csv_batches(
    records: list[PinRecord],
    output_dir: Path,
    batch_size: int = 50,
    prefix: str = "pinterest_pins",
) -> list[Path]:
    if batch_size <= 0:
        raise ValueError("batch_size must be greater than 0")

    output_dir.mkdir(parents=True, exist_ok=True)
    generated_files: list[Path] = []

    for batch_index, start in enumerate(range(0, len(records), batch_size), start=1):
        output_path = output_dir / f"{prefix}_batch_{batch_index:03}.csv"
        batch_records = records[start : start + batch_size]

        with output_path.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=PINTEREST_HEADERS)
            writer.writeheader()
            for record in batch_records:
                writer.writerow(_pin_record_to_row(record))

        generated_files.append(output_path)

    return generated_files


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
