from __future__ import annotations

from pathlib import Path

from pin_generator.config import AppConfig
from pin_generator.models import PinRecord
from pin_generator.services.csv_exporter import save_pinterest_csv_batches, save_upload_manifest
from pin_generator.services.image_discovery import discover_images, make_public_media_url
from pin_generator.services.csv_exporter import save_pinterest_csv, save_upload_manifest
from pin_generator.services.image_discovery import discover_sku_mockups, make_public_media_url
from pin_generator.services.keyword_selector import load_keyword_bank, select_keywords
from pin_generator.services.text_generator import build_title, detect_etsy_link


def generate_pins(config: AppConfig, etsy_mapping_file: Path | None = None) -> tuple[list[PinRecord], list[Path]]:
    print("[generate_pins] Starting pipeline...")
    print(f"[generate_pins] input_images_dir: {config.input_images_dir.resolve()}")
    print(f"[generate_pins] keyword_bank_path: {config.keyword_bank_path.resolve()}")
    print(f"[generate_pins] output_csv_path: {config.output_csv_path.resolve()}")
    print(f"[generate_pins] output_manifest_path: {config.output_images_manifest.resolve()}")
    print(f"[generate_pins] etsy_mapping_file: {etsy_mapping_file.resolve() if etsy_mapping_file else '<none>'}")
    print(f"[generate_pins] default_pin_description length: {len(config.default_pin_description)}")

    assets = discover_images(config.input_images_dir)
    keyword_bank = load_keyword_bank(config.keyword_bank_path)
    print(f"[generate_pins] Loaded {len(keyword_bank)} keywords from bank.")

    records: list[PinRecord] = []
    for idx, asset in enumerate(assets, start=1):
        print(f"[generate_pins] Building record {idx}/{len(assets)} for file: {asset.local_path}")
        title = build_title(asset.file_stem)
        description = config.default_pin_description[: config.max_description_chars]
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
                description=description,
                link=detect_etsy_link(asset.file_stem, etsy_mapping_file),
                publish_date="",
                keywords=", ".join(selected),
            )
        )

    print(f"[generate_pins] Built {len(records)} records. Writing CSV batches...")
    generated_batches = save_pinterest_csv_batches(
        records=records,
        output_dir=config.output_csv_path.parent,
        batch_size=50,
        prefix=config.output_csv_path.stem,
    )
    print(f"[generate_pins] CSV batches written: {len(generated_batches)}")

    save_upload_manifest(assets, config.media_base_url, config.output_images_manifest)
    print("[generate_pins] Upload manifest written.")
    print("[generate_pins] Pipeline finished.")
    return records, generated_batches
