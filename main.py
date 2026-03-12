from pathlib import Path

from pin_generator.config import DEFAULT_CONFIG
from pin_generator.pipelines.generate_pins import generate_pins


def main() -> None:
    config = DEFAULT_CONFIG

    # Optional map file with specific Etsy URLs per image stem.
    # Format: file_stem,etsy_url
    etsy_mapping_file = Path("data/input/etsy_links.csv")

    records = generate_pins(config=config, etsy_mapping_file=etsy_mapping_file)
    print(f"Generated {len(records)} pin records -> {config.output_csv_path}")
    print(f"Upload helper manifest -> {config.output_images_manifest}")


if __name__ == "__main__":
    main()
