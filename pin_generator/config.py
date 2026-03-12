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
    max_keywords_per_pin: int = 8
    max_description_chars: int = 500
    mockup_selection_seed: int | None = None


DEFAULT_CONFIG = AppConfig(
    input_images_dir=Path("data/input/mockups"),
    keyword_bank_path=Path("data/input/keywords.txt"),
    board_name="my-pinterest-board",
    media_base_url="https://your-domain.com/pins",
    output_csv_path=Path("data/output/pinterest_pins.csv"),
    output_images_manifest=Path("data/output/image_upload_manifest.csv"),
)
