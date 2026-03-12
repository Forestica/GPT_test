from __future__ import annotations

from pathlib import Path


def build_title(file_stem: str) -> str:
    words = file_stem.replace("_", " ").replace("-", " ").strip()
    return words.title() if words else "Art Print"


def build_description(file_stem: str, etsy_shop_name: str = "Your Etsy Shop") -> str:
    readable = build_title(file_stem)
    template = (
        f"Discover {readable} – printable wall art ideal for cozy interiors,"
        f" gallery walls and gift ideas. Explore more designs in {etsy_shop_name}."
    )
    return template[:500]


def detect_etsy_link(file_stem: str, mapping_file: Path | None = None) -> str:
    """
    Optional map: CSV with columns `file_stem,etsy_url`.
    Fallback returns shop homepage.
    """
    if mapping_file and mapping_file.exists():
        for line in mapping_file.read_text(encoding="utf-8").splitlines()[1:]:
            if not line.strip():
                continue
            stem, etsy_url = [x.strip() for x in line.split(",", maxsplit=1)]
            if stem == file_stem and etsy_url:
                return etsy_url
    return "https://www.etsy.com/shop/YourShopName"
