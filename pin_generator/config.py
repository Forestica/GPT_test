from dataclasses import dataclass
from pathlib import Path


@dataclass
class AppConfig:
    input_images_dir: Path
    keyword_bank_path: Path
    board_name: str
    media_base_url: str
    output_csv_path: Path
    output_images_manifest: Path
    default_pin_description: str
    max_keywords_per_pin: int = 8
    max_description_chars: int = 500


DEFAULT_CONFIG = AppConfig(
    input_images_dir=Path("data/input/mockups"),
    keyword_bank_path=Path("data/input/keywords.txt"),
    board_name="my-pinterest-board",
    media_base_url="https://your-domain.com/pins",
    output_csv_path=Path("data/output/pinterest_pins.csv"),
    output_images_manifest=Path("data/output/image_upload_manifest.csv"),
    default_pin_description=(
        "Printable wall art for cozy interiors, gallery walls, and thoughtful gifts. "
        "Instant digital download ready to print at home or with a local print shop."
    ),
)
