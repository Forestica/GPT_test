from __future__ import annotations

from pathlib import Path

from pin_generator.config import AppConfig
from pin_generator.models import PinRecord
from pin_generator.services.csv_exporter import save_pinterest_csv, save_upload_manifest
from pin_generator.services.image_discovery import discover_images, make_public_media_url
from pin_generator.services.keyword_selector import load_keyword_bank, select_keywords
from pin_generator.services.text_generator import build_description, build_title, detect_etsy_link


def generate_pins(config: AppConfig, etsy_mapping_file: Path | None = None) -> list[PinRecord]:
    assets = discover_images(config.input_images_dir)
    keyword_bank = load_keyword_bank(config.keyword_bank_path)

    records: list[PinRecord] = []
    for asset in assets:
        title = build_title(asset.file_stem)
        description = build_description(asset.file_stem)
        selected = select_keywords(
            image_name=asset.file_stem,
            description=description,
            keyword_bank=keyword_bank,
            max_keywords=config.max_keywords_per_pin,
        )

        records.append(
            PinRecord(
                title=title,
                media_url=make_public_media_url(asset.local_path, config.media_base_url),
                pinterest_board=config.board_name,
                thumbnail="",
                description=description[: config.max_description_chars],
                link=detect_etsy_link(asset.file_stem, etsy_mapping_file),
                publish_date="",
                keywords=", ".join(selected),
            )
        )

    save_pinterest_csv(records, config.output_csv_path)
    save_upload_manifest(assets, config.media_base_url, config.output_images_manifest)
    return records
