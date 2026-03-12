import random
from pathlib import Path

from pin_generator.models import ImageAsset, SkuImageAsset

SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg"}


def discover_images(images_dir: Path) -> list[ImageAsset]:
    assets: list[ImageAsset] = []
    for path in sorted(images_dir.glob("*")):
        if path.suffix.lower() in SUPPORTED_EXTENSIONS and path.is_file():
            assets.append(ImageAsset(local_path=path, file_stem=path.stem))
    return assets


def discover_sku_mockups(root_dir: Path, seed: int | None = None) -> list[SkuImageAsset]:
    rng = random.Random(seed)
    assets: list[SkuImageAsset] = []

    for sku_dir in sorted(path for path in root_dir.iterdir() if path.is_dir()):
        mockup_dir = next(
            (child for child in sku_dir.iterdir() if child.is_dir() and child.name.lower() == "mockups"),
            None,
        )
        if mockup_dir is None:
            continue

        candidates = sorted(
            path
            for path in mockup_dir.rglob("*")
            if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
        )
        if not candidates:
            continue

        selected = rng.choice(candidates)
        sku_id, sku_name = _parse_sku_folder_name(sku_dir.name)
        assets.append(
            SkuImageAsset(
                sku_id=sku_id,
                sku_name=sku_name,
                local_path=selected,
                file_stem=selected.stem,
            )
        )

    return assets


def _parse_sku_folder_name(folder_name: str) -> tuple[str, str]:
    parts = folder_name.split(" - ", maxsplit=1)
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    return folder_name.strip(), folder_name.strip()


def make_public_media_url(local_path: Path, media_base_url: str) -> str:
    """
    Pinterest CSV expects a public URL.
    We map local filename to a future uploaded URL:
    https://your-domain.com/pins/my_file.png
    """
    return f"{media_base_url.rstrip('/')}/{local_path.name}"
